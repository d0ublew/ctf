void UndefinedFunction_00000000(longlong param_1)

{
    int iVar1;
    int iVar2;
    undefined8 uVar3;
    undefined8 uStackX_8;

    *(undefined4 *)(*(longlong *)(param_1 + 0x108) + 8) = 3;
    uVar3 = (**(code **)(param_1 + 0x390))(
        param_1, *(undefined4 *)(*(longlong *)(param_1 + 0x108) + 8));
    uStackX_8 = 0;
    iVar1 = (**(code **)(param_1 + 0x380))(uVar3, &uStackX_8, 4);
    iVar2 = (**(code **)(param_1 + 0x388))(uStackX_8, 0x20);
    if (iVar2 == iVar1) {
        (**(code **)(param_1 + 0x350))(iVar1 * 1000);
    } else {
        (**(code **)(param_1 + 0x358))(
            *(undefined4 *)(*(longlong *)(param_1 + 0x108) + 8));
    }
    (**(code **)(param_1 + 0x368))(uVar3);
    (**(code **)(param_1 + 0x3b0))(param_1);
    return;
}
