#include <windows.h>
#include <stdio.h>
#include "MinHook.h"

char *gData;
int gLen = 0;
DWORD __stdcall my_GetModuleFileNameA(HMODULE hModule, LPSTR lpFilename, DWORD nSize);
DWORD (__stdcall *orig_GetModuleFileNameA)(HMODULE hModule, LPSTR lpFilename, DWORD nSize) = GetModuleFileNameA;
BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
      )
{
if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
#define makehook(x) MH_CreateHook(&(x), &(my_##x), (void **)&(orig_##x))
if (MH_Initialize() != MH_OK) return FALSE;
makehook(GetModuleFileNameA);
}
    return TRUE;
}

DWORD __stdcall my_GetModuleFileNameA(HMODULE hModule, LPSTR lpFilename, DWORD nSize)
{
DWORD res = orig_GetModuleFileNameA(hModule, lpFilename, nSize);
//printf("hm=%p lpFilename=%s\n", hModule, lpFilename);
if (hModule == NULL) {
strncpy(lpFilename, gData, strlen(gData));
lpFilename[strlen(gData)] = '\0';
//printf("lfn now %s\n", lpFilename);
return strlen(gData);
}
return res;
}

int __stdcall SetData(char *data) {
if (gData != NULL) {
free(gData);
gData = NULL;
}
gData = (char *)malloc(strlen(data) + 1);
memset(gData, 0, strlen(data)+1);
strncpy(gData, data, strlen(data));
return 0;
}

void __stdcall Hook() {
MH_EnableHook(MH_ALL_HOOKS);
}
void __stdcall Unhook() {
MH_DisableHook(MH_ALL_HOOKS);
}
