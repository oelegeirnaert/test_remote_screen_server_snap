import os
import psutil
import platform
from datetime import datetime
from Xlib import display
import json


def get_snap_info():
    SNAP_ARCH = os.environ.get("SNAP_ARCH", "unknown")
    SNAP_NAME = os.environ.get("SNAP_NAME", "unknown")
    SNAP_REVISION = os.environ.get("SNAP_REVISION", "unknown")
    SNAP_VERSION = os.environ.get("SNAP_VERSION", "unknown")

    info = {
        "arc": SNAP_ARCH,
        "name": SNAP_NAME,
        "revision": SNAP_REVISION,
        "version": SNAP_VERSION,
    }
    print(info)

    return info


def get_machine_id():
    try:
        machineId = os.popen("cat /etc/machine-id")
        machineId = machineId.read()
        if "\n" in machineId:
            machineId = machineId.replace("\n", "")
        return machineId
    except Exception as exc:
        print(str(exc))

    return None


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_platform_info():
    print("=" * 40, "System Information", "=" * 40)
    uname = platform.uname()
    info = {
        "system": uname.system,
        "node_name": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "machine_id": get_machine_id(),
    }
    print(info)

    return info


def get_boot_time_info():
    # Boot Time
    print("=" * 40, "Boot Time", "=" * 40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    return {"boot_time": str(bt)}


def get_cpu_info():
    # let's print CPU information
    print("=" * 40, "CPU Info", "=" * 40)
    # number of cores
    cpufreq = psutil.cpu_freq()

    info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": f"{cpufreq.max:.2f}Mhz",
        "min_frequency": f"{cpufreq.min:.2f}Mhz",
        "current_frequency": f"{cpufreq.current:.2f}Mhz",
    }

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    # CPU usage
    print("CPU Usage Per Core:")

    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    print(info)

    return info


def get_memory_info():
    # Memory Information
    print("=" * 40, "Memory Information", "=" * 40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("=" * 20, "SWAP", "=" * 20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")


def get_disk_info():
    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")


def get_network_info():
    # Network information
    print("=" * 40, "Network Information", "=" * 40)
    # get all network interfaces (virtual and physical)
    interfaces = []
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            info = {
                "address_family": address.family,
                "interface_name": interface_name,
                "ip_address": address.address,
                "netmask": address.netmask,
                "broadcast_ip": address.broadcast,
            }
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == "AddressFamily.AF_INET":
                info = {
                    "ip_address": address.address,
                    "netmask": address.netmask,
                    "broadcast_ip": address.broadcast,
                }
                interfaces.append(info)
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == "AddressFamily.AF_PACKET":
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

    info = {
        "total_bytes_sent": get_size(net_io.bytes_sent),
        "total_bytes_received": get_size(net_io.bytes_recv),
        "interfaces": interfaces,
    }

    return info


def get_monitor_info():
    try:
        d = display.Display()
    except Exception as exc:
        print("NO SCREENS")
        print(str(exc))
        return

    screen_count = d.screen_count()
    print(f"screens: {screen_count}")
    if screen_count == 0:
        print("NO SCREENS ATTACHED!")
        return

    default_screen = d.get_default_screen()
    print("=" * 40, "Monitor Information", "=" * 40)
    for screen in range(0, screen_count):
        info = d.screen(screen)
        print("Screen: %s. Default: %s" % (screen, screen == default_screen))
        print("Width: %s, height: %s" % (info.width_in_pixels, info.height_in_pixels))


def get_all_info():
    get_snap_info()
    get_platform_info()
    get_boot_time_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    get_monitor_info()
