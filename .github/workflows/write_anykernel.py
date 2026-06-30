#!/usr/bin/env python3
"""Write anykernel.sh with correct content for munch device."""
import sys

content = """# AnyKernel3 Ramdisk Mod Script
properties() { '
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=munch
device.name2=munchin
device.name3=RedmiK40S
device.name4=POCOF4
supported.versions=
supported.patchlevels=
'; }
block=boot;
is_slot_device=auto;
ramdisk_compression=auto;
patch_vbmeta_flag=auto;

. tools/ak3-core.sh;

userflavor=$(file_getprop /system/build.prop "ro.build.flavor");
if [ -z "$userflavor" ]; then
  userflavor=$(file_getprop /system/system/build.prop "ro.build.flavor");
fi;
case $userflavor in
    missi*|qssi*) os=miui; os_string="HyperOS/MIUI ROM";;
    crdroid_*) os=aosp; os_string="crDroid ROM";;
    *) os=aosp; os_string="AOSP ROM";;
esac;
ui_print "  -> $os_string detected!";

mv $home/kernels/Image $home/Image;
[ -f $home/kernels/dtb ] && mv $home/kernels/dtb $home/dtb;
[ -f $home/kernels/dtbo ] && mv $home/kernels/dtbo $home/dtbo;

# use write_boot to handle boot + vendor_boot + vendor_dlkm + dtbo
write_boot;
"""

path = sys.argv[1]
with open(path, 'w') as f:
    f.write(content)
print(f"Written {len(content)} bytes to {path}")
