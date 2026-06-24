#!/usr/bin/env python3
"""Write anykernel.sh with correct content for munch device."""
import sys

content = """# AnyKernel3 Ramdisk Mod Script
properties() { '
do.devicecheck=1
do.modules=1
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=munch
device.name2=munchin
device.name3=RedmiK40S
device.name4=POCOF4
device.name5=alioth
device.name6=apollo
device.name7=lmi
supported.versions=
supported.patchlevels=
'; }
block=boot;
is_slot_device=auto;
ramdisk_compression=auto;
patch_vbmeta_flag=auto;
no_block_display=1;

. tools/ak3-core.sh;

userflavor=$(file_getprop /system/build.prop "ro.build.flavor");
case $userflavor in
    missi*|qssi*) os=miui; os_string="HyperOS/MIUI ROM";;
    crdroid_*) os=aosp; os_string="crDroid ROM";;
    *) os=aosp; os_string="AOSP ROM";;
esac;
ui_print "  -> $os_string is detected!";

# 复制内核镜像和设备树到根目录
mv $home/kernels/Image $home/Image;
[ -f $home/kernels/dtb ] && mv $home/kernels/dtb $home/dtb;
[ -f $home/kernels/dtbo ] && mv $home/kernels/dtbo $home/dtbo;

# 刷入 boot 分区
split_boot;
flash_boot;

# 如果有 dtbo 则刷入
[ -f $home/dtbo ] && flash_dtbo;
"""

path = sys.argv[1]
with open(path, 'w') as f:
    f.write(content)
print(f"Written {len(content)} bytes to {path}")
