#!/usr/bin/env python3.6
from insights import dr
from insights.formats.text import HumanReadableFormat as Formatter
# from insights.formats._json import JsonFormatter as Formatter

from insights.specs import Specs
from insights.tests import context_wrap



MSGINFO = """
BUG: soft lockup - CPU#0 stuck for 67s! [clearcache.sh:4383]
Modules linked in: nfs lockd fscache auth_rpcgss nfs_acl symap_rh_ES_6_2_6_32_431_el6_x86_64(P)(U) symev_rh_ES_6_2_6_32_431_el6_x86_64(U) sunrpc vsock(U) ipv6 ppdev parport_pc parport vmware_balloon sg vmci(U) i2c_piix4 shpchp ext4 jbd2 mbcache sr_mod cdrom sd_mod crc_t10dif ahci vmxnet3 mptsas mptscsih mptbase scsi_transport_sas pata_acpi ata_generic ata_piix vmwgfx ttm drm_kms_helper drm i2c_core dm_mirror dm_region_hash dm_log dm_mod [last unloaded: scsi_wait_scan]
CPU 0
Modules linked in: nfs lockd fscache auth_rpcgss nfs_acl symap_rh_ES_6_2_6_32_431_el6_x86_64(P)(U) symev_rh_ES_6_2_6_32_431_el6_x86_64(U) sunrpc vsock(U) ipv6 ppdev parport_pc parport vmware_balloon sg vmci(U) i2c_piix4 shpchp ext4 jbd2 mbcache sr_mod cdrom sd_mod crc_t10dif ahci vmxnet3 mptsas mptscsih mptbase scsi_transport_sas pata_acpi ata_generic ata_piix vmwgfx ttm drm_kms_helper drm i2c_core dm_mirror dm_region_hash dm_log dm_mod [last unloaded: scsi_wait_scan]

Pid: 4383, comm: clearcache.sh Tainted: P           --L------------    2.6.32-696.23.1.el6.x86_64 #1 VMware, Inc. VMware Virtual Platform/440BX Desktop Reference Platform
RIP: 0010:[<ffffffff812a442c>]  [<ffffffff812a442c>] __lookup+0x3c/0xe0
RSP: 0018:ffff88013c3e3c00  EFLAGS: 00000287
RAX: 0000000000000000 RBX: ffff88013c3e3c18 RCX: 0000000000000006
RDX: 0000000000000000 RSI: ffff88013c3e3d38 RDI: ffff8800b13e0050
RBP: ffffffff8155f13e R08: 000000000000000e R09: ffff88013c3e3c38
R10: 0000000000000016 R11: 0000000000000002 R12: 0000000000000000
R13: ffff88013bd0e6e0 R14: ffff88013fffbc18 R15: 0000000000000000
FS:  00007fa539da0700(0000) GS:ffff880028200000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 00007fa539dab000 CR3: 000000013cf48000 CR4: 00000000000607f0
DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
DR3: 0000000000000000 DR6: 00000000ffff0ff0 DR7: 0000000000000400
Process clearcache.sh (pid: 4383, threadinfo ffff88013c3e0000, task ffff88013c056ab0)
Stack:
 0000000000000000 000000000000000e 0000000000000000 ffff88013c3e3c68
<d> ffffffff812a4641 0000000000000fff 000000000000000e 0000000000000024
<d> ffff88013c3e3d38 0000000000000016 000000000000000e 000000000000000e
Call Trace:
 [<ffffffff812a4641>] ? radix_tree_gang_lookup_slot+0x81/0xf0
 [<ffffffff81130c0b>] ? find_get_pages+0x3b/0x150
 [<ffffffff81147432>] ? pagevec_lookup+0x22/0x30
 [<ffffffff81148f44>] ? invalidate_mapping_pages+0x84/0x1e0
 [<ffffffff811cc2ee>] ? drop_caches_sysctl_handler+0x12e/0x1d0
 [<ffffffff81213e9c>] ? proc_sys_call_handler+0x9c/0xd0
 [<ffffffff81213ee4>] ? proc_sys_write+0x14/0x20
 [<ffffffff8119cb5a>] ? vfs_write+0xba/0x1a0
 [<ffffffff8119e056>] ? fget_light_pos+0x16/0x50
 [<ffffffff8119d691>] ? sys_write+0x51/0xb0
 [<ffffffffa03eea23>] ? symev_write+0x53/0xa0 [symev_rh_ES_6_2_6_32_431_el6_x86_64]
 [<ffffffff8155e351>] ? system_call_fastpath+0x2f/0x34
""".strip()

dr.load_components("rules")
dr.load_components("insights.specs.default")
# Below 3 components are not working as it's based on python2
#dr.load_components("telemetry")
#dr.load_components("diag_insights_rules")
#dr.load_components("prodsec")
dr.load_components("support-rules")
broker = dr.Broker()
broker[Specs.hostname] = context_wrap("www.example.com")
#broker[Specs.kernel] = context_wrap("2.6.32-696.23.1.el6.x86_64")
broker[Specs.uname] = context_wrap("Linux a03a5df6f247 2.6.32-696.23.1.el6.x86_64 #1 SMP Wed Jun 6 16:55:56 UTC 2018 x86_64 GNU/Linux")
broker[Specs.dmesg] = context_wrap(MSGINFO)
with Formatter(broker):
    dr.run(broker=broker)
