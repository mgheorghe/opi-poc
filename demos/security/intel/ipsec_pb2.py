# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ipsec.proto
# Protobuf Python Version: 4.25.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bipsec.proto\x12\x13opi_api.security.v1\"\x80\x02\n\tProposals\x12\x43\n\ncrypto_alg\x18\x01 \x03(\x0e\x32$.opi_api.security.v1.CryptoAlgorithmR\tcryptoAlg\x12@\n\tinteg_alg\x18\x02 \x03(\x0e\x32#.opi_api.security.v1.IntegAlgorithmR\x08integAlg\x12\x31\n\x03prf\x18\x03 \x03(\x0e\x32\x1f.opi_api.security.v1.PRFunctionR\x03prf\x12\x39\n\x08\x64hgroups\x18\x04 \x03(\x0e\x32\x1d.opi_api.security.v1.DHGroupsR\x08\x64hgroups\"\x18\n\x04Vips\x12\x10\n\x03vip\x18\x01 \x03(\tR\x03vip\"\x1b\n\x05Pools\x12\x12\n\x04pool\x18\x01 \x03(\tR\x04pool\"\x1b\n\x05\x43\x65rts\x12\x12\n\x04\x63\x65rt\x18\x01 \x03(\tR\x04\x63\x65rt\"!\n\x07PubKeys\x12\x16\n\x06pubkey\x18\x01 \x03(\tR\x06pubkey\"\x1e\n\x06Groups\x12\x14\n\x05group\x18\x01 \x03(\tR\x05group\"-\n\nCertPolicy\x12\x1f\n\x0b\x63\x65rt_policy\x18\x01 \x03(\tR\ncertPolicy\"!\n\x07\x43\x61\x43\x65rts\x12\x16\n\x06\x63\x61\x63\x65rt\x18\x01 \x03(\tR\x06\x63\x61\x63\x65rt\"\x81\x02\n\tLocalAuth\x12\x31\n\x04\x61uth\x18\x01 \x01(\x0e\x32\x1d.opi_api.security.v1.AuthTypeR\x04\x61uth\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\x12\x15\n\x06\x65\x61p_id\x18\x03 \x01(\tR\x05\x65\x61pId\x12\x15\n\x06\x61\x61\x61_id\x18\x04 \x01(\tR\x05\x61\x61\x61Id\x12\x19\n\x08xauth_id\x18\x05 \x01(\tR\x07xauthId\x12\x30\n\x05\x63\x65rts\x18\x06 \x01(\x0b\x32\x1a.opi_api.security.v1.CertsR\x05\x63\x65rts\x12\x36\n\x07pubkeys\x18\x07 \x01(\x0b\x32\x1c.opi_api.security.v1.PubKeysR\x07pubkeys\"\x80\x03\n\nRemoteAuth\x12\x31\n\x04\x61uth\x18\x01 \x01(\x0e\x32\x1d.opi_api.security.v1.AuthTypeR\x04\x61uth\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\x12\x15\n\x06\x65\x61p_id\x18\x03 \x01(\tR\x05\x65\x61pId\x12\x33\n\x06groups\x18\x04 \x01(\x0b\x32\x1b.opi_api.security.v1.GroupsR\x06groups\x12@\n\x0b\x63\x65rt_policy\x18\x05 \x01(\x0b\x32\x1f.opi_api.security.v1.CertPolicyR\ncertPolicy\x12\x30\n\x05\x63\x65rts\x18\x06 \x01(\x0b\x32\x1a.opi_api.security.v1.CertsR\x05\x63\x65rts\x12\x37\n\x08\x63\x61_certs\x18\x07 \x01(\x0b\x32\x1c.opi_api.security.v1.CaCertsR\x07\x63\x61\x43\x65rts\x12\x36\n\x07pubkeys\x18\x08 \x01(\x0b\x32\x1c.opi_api.security.v1.PubKeysR\x07pubkeys\"\xaa\x01\n\x10TrafficSelectors\x12\x45\n\x02ts\x18\x01 \x03(\x0b\x32\x35.opi_api.security.v1.TrafficSelectors.TrafficSelectorR\x02ts\x1aO\n\x0fTrafficSelector\x12\x12\n\x04\x63idr\x18\x01 \x01(\tR\x04\x63idr\x12\x14\n\x05proto\x18\x02 \x01(\tR\x05proto\x12\x12\n\x04port\x18\x03 \x01(\tR\x04port\"\x1b\n\x05\x41\x64\x64rs\x12\x12\n\x04\x61\x64\x64r\x18\x01 \x01(\tR\x04\x61\x64\x64r\"\xed\x04\n\x05\x43hild\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x41\n\x0c\x61g_proposals\x18\x02 \x01(\x0b\x32\x1e.opi_api.security.v1.ProposalsR\x0b\x61gProposals\x12\x43\n\resp_proposals\x18\x03 \x01(\x0b\x32\x1e.opi_api.security.v1.ProposalsR\x0c\x65spProposals\x12@\n\x08local_ts\x18\x04 \x01(\x0b\x32%.opi_api.security.v1.TrafficSelectorsR\x07localTs\x12\x42\n\tremote_ts\x18\x05 \x01(\x0b\x32%.opi_api.security.v1.TrafficSelectorsR\x08remoteTs\x12\x1d\n\nrekey_time\x18\x06 \x01(\rR\trekeyTime\x12\x1b\n\tlife_time\x18\x07 \x01(\rR\x08lifeTime\x12\x1b\n\trand_time\x18\x08 \x01(\rR\x08randTime\x12\x16\n\x06updown\x18\t \x01(\tR\x06updown\x12\x1e\n\ninactivity\x18\n \x01(\rR\ninactivity\x12\x17\n\x07mark_in\x18\x0b \x01(\rR\x06markIn\x12\x1c\n\nmark_in_sa\x18\x0c \x01(\tR\x08markInSa\x12\x19\n\x08mark_out\x18\r \x01(\rR\x07markOut\x12\x1e\n\x0bset_mark_in\x18\x0e \x01(\rR\tsetMarkIn\x12 \n\x0cset_mark_out\x18\x0f \x01(\rR\nsetMarkOut\x12\x1d\n\nhw_offload\x18\x10 \x01(\tR\thwOffload\"\x8e\x06\n\nConnection\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x18\n\x07version\x18\x02 \x01(\tR\x07version\x12;\n\x0blocal_addrs\x18\x03 \x03(\x0b\x32\x1a.opi_api.security.v1.AddrsR\nlocalAddrs\x12=\n\x0cremote_addrs\x18\x04 \x03(\x0b\x32\x1a.opi_api.security.v1.AddrsR\x0bremoteAddrs\x12\x1d\n\nlocal_port\x18\x05 \x01(\rR\tlocalPort\x12\x1f\n\x0bremote_port\x18\x06 \x01(\rR\nremotePort\x12<\n\tproposals\x18\x07 \x01(\x0b\x32\x1e.opi_api.security.v1.ProposalsR\tproposals\x12-\n\x04vips\x18\x08 \x01(\x0b\x32\x19.opi_api.security.v1.VipsR\x04vips\x12\x12\n\x04\x64scp\x18\t \x01(\x04R\x04\x64scp\x12\x14\n\x05\x65ncap\x18\n \x01(\tR\x05\x65ncap\x12\x16\n\x06mobike\x18\x0b \x01(\tR\x06mobike\x12\x1b\n\tdpd_delay\x18\x0c \x01(\rR\x08\x64pdDelay\x12\x1f\n\x0b\x64pd_timeout\x18\r \x01(\rR\ndpdTimeout\x12\x1f\n\x0breauth_time\x18\x0e \x01(\rR\nreauthTime\x12\x1d\n\nrekey_time\x18\x0f \x01(\rR\trekeyTime\x12\x30\n\x05pools\x18\x10 \x01(\x0b\x32\x1a.opi_api.security.v1.PoolsR\x05pools\x12=\n\nlocal_auth\x18\x11 \x01(\x0b\x32\x1e.opi_api.security.v1.LocalAuthR\tlocalAuth\x12@\n\x0bremote_auth\x18\x12 \x01(\x0b\x32\x1f.opi_api.security.v1.RemoteAuthR\nremoteAuth\x12\x36\n\x08\x63hildren\x18\x13 \x03(\x0b\x32\x1a.opi_api.security.v1.ChildR\x08\x63hildren\"\x15\n\x13IPsecVersionRequest\"\x96\x01\n\x14IPsecVersionResponse\x12\x16\n\x06\x64\x61\x65mon\x18\x01 \x01(\tR\x06\x64\x61\x65mon\x12\x18\n\x07version\x18\x02 \x01(\tR\x07version\x12\x18\n\x07sysname\x18\x03 \x01(\tR\x07sysname\x12\x18\n\x07release\x18\x04 \x01(\tR\x07release\x12\x18\n\x07machine\x18\x05 \x01(\tR\x07machine\"\x13\n\x11IPsecStatsRequest\",\n\x12IPsecStatsResponse\x12\x16\n\x06status\x18\x01 \x01(\tR\x06status\"t\n\x14IPsecInitiateRequest\x12\x14\n\x05\x63hild\x18\x01 \x01(\tR\x05\x63hild\x12\x10\n\x03ike\x18\x02 \x01(\tR\x03ike\x12\x18\n\x07timeout\x18\x03 \x01(\tR\x07timeout\x12\x1a\n\x08loglevel\x18\x04 \x01(\tR\x08loglevel\"\x17\n\x15IPsecInitiateResponse\"\xbd\x01\n\x15IPsecTerminateRequest\x12\x14\n\x05\x63hild\x18\x01 \x01(\tR\x05\x63hild\x12\x10\n\x03ike\x18\x02 \x01(\tR\x03ike\x12\x19\n\x08\x63hild_id\x18\x03 \x01(\x04R\x07\x63hildId\x12\x15\n\x06ike_id\x18\x04 \x01(\x04R\x05ikeId\x12\x14\n\x05\x66orce\x18\x05 \x01(\tR\x05\x66orce\x12\x18\n\x07timeout\x18\x06 \x01(\tR\x07timeout\x12\x1a\n\x08loglevel\x18\x07 \x01(\tR\x08loglevel\"l\n\x16IPsecTerminateResponse\x12\x18\n\x07success\x18\x01 \x01(\tR\x07success\x12\x18\n\x07matches\x18\x02 \x01(\rR\x07matches\x12\x1e\n\nterminated\x18\x03 \x01(\rR\nterminated\"\x85\x01\n\x11IPsecRekeyRequest\x12\x14\n\x05\x63hild\x18\x01 \x01(\tR\x05\x63hild\x12\x10\n\x03ike\x18\x02 \x01(\tR\x03ike\x12\x19\n\x08\x63hild_id\x18\x03 \x01(\x04R\x07\x63hildId\x12\x15\n\x06ike_id\x18\x04 \x01(\x04R\x05ikeId\x12\x16\n\x06reauth\x18\x05 \x01(\tR\x06reauth\"H\n\x12IPsecRekeyResponse\x12\x18\n\x07success\x18\x01 \x01(\tR\x07success\x12\x18\n\x07matches\x18\x02 \x01(\rR\x07matches\"\x89\x01\n\x13IPsecListSasRequest\x12\x18\n\x07noblock\x18\x01 \x01(\tR\x07noblock\x12\x10\n\x03ike\x18\x02 \x01(\tR\x03ike\x12\x15\n\x06ike_id\x18\x03 \x01(\x04R\x05ikeId\x12\x14\n\x05\x63hild\x18\x04 \x01(\tR\x05\x63hild\x12\x19\n\x08\x63hild_id\x18\x05 \x01(\x04R\x07\x63hildId\"\x90\x04\n\x0bListChildSa\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x1a\n\x08protocol\x18\x02 \x01(\tR\x08protocol\x12\x14\n\x05\x65ncap\x18\x03 \x01(\tR\x05\x65ncap\x12\x15\n\x06spi_in\x18\x04 \x01(\tR\x05spiIn\x12\x17\n\x07spi_out\x18\x05 \x01(\tR\x06spiOut\x12\x15\n\x06\x63pi_in\x18\x06 \x01(\tR\x05\x63piIn\x12\x17\n\x07\x63pi_out\x18\x07 \x01(\tR\x06\x63piOut\x12\x17\n\x07mark_in\x18\x08 \x01(\tR\x06markIn\x12 \n\x0cmark_mask_in\x18\t \x01(\tR\nmarkMaskIn\x12\x19\n\x08mark_out\x18\n \x01(\tR\x07markOut\x12\"\n\rmark_mask_out\x18\x0b \x01(\tR\x0bmarkMaskOut\x12\x18\n\x08if_id_in\x18\x0c \x01(\tR\x06ifIdIn\x12\x1a\n\tif_id_out\x18\r \x01(\tR\x07ifIdOut\x12\x19\n\x08\x65ncr_alg\x18\x0e \x01(\tR\x07\x65ncrAlg\x12!\n\x0c\x65ncr_keysize\x18\x0f \x01(\tR\x0b\x65ncrKeysize\x12\x1b\n\tinteg_alg\x18\x10 \x01(\tR\x08integAlg\x12#\n\rinteg_keysize\x18\x11 \x01(\tR\x0cintegKeysize\x12\x19\n\x08\x64h_group\x18\x12 \x01(\tR\x07\x64hGroup\x12\x10\n\x03\x65sn\x18\x13 \x01(\tR\x03\x65sn\"\xb5\t\n\tListIkeSa\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x1a\n\x08uniqueid\x18\x02 \x01(\tR\x08uniqueid\x12\x18\n\x07version\x18\x03 \x01(\tR\x07version\x12;\n\x08ikestate\x18\x04 \x01(\x0e\x32\x1f.opi_api.security.v1.IkeSaStateR\x08ikestate\x12\x1d\n\nlocal_host\x18\x05 \x01(\tR\tlocalHost\x12\x1d\n\nlocal_port\x18\x06 \x01(\tR\tlocalPort\x12\x19\n\x08local_id\x18\x07 \x01(\tR\x07localId\x12\x1f\n\x0bremote_host\x18\x08 \x01(\tR\nremoteHost\x12\x1f\n\x0bremote_port\x18\t \x01(\tR\nremotePort\x12\x1b\n\tremote_id\x18\n \x01(\tR\x08remoteId\x12&\n\x0fremote_xauth_id\x18\x0b \x01(\tR\rremoteXauthId\x12\"\n\rremote_eap_id\x18\x0c \x01(\tR\x0bremoteEapId\x12\x1c\n\tinitiator\x18\r \x01(\tR\tinitiator\x12#\n\rinitiator_spi\x18\x0e \x01(\tR\x0cinitiatorSpi\x12#\n\rresponder_spi\x18\x0f \x01(\tR\x0cresponderSpi\x12\x1b\n\tnat_local\x18\x10 \x01(\tR\x08natLocal\x12\x1d\n\nnat_remote\x18\x11 \x01(\tR\tnatRemote\x12\x19\n\x08nat_fake\x18\x12 \x01(\tR\x07natFake\x12\x17\n\x07nat_any\x18\x13 \x01(\tR\x06natAny\x12\x18\n\x08if_id_in\x18\x14 \x01(\tR\x06ifIdIn\x12\x1a\n\tif_id_out\x18\x15 \x01(\tR\x07ifIdOut\x12\x19\n\x08\x65ncr_alg\x18\x16 \x01(\tR\x07\x65ncrAlg\x12!\n\x0c\x65ncr_keysize\x18\x17 \x01(\tR\x0b\x65ncrKeysize\x12\x1b\n\tinteg_alg\x18\x18 \x01(\tR\x08integAlg\x12#\n\rinteg_keysize\x18\x19 \x01(\tR\x0cintegKeysize\x12\x17\n\x07prf_alg\x18\x1a \x01(\tR\x06prfAlg\x12\x19\n\x08\x64h_group\x18\x1b \x01(\tR\x07\x64hGroup\x12\x10\n\x03ppk\x18\x1c \x01(\tR\x03ppk\x12 \n\x0b\x65stablished\x18\x1d \x01(\tR\x0b\x65stablished\x12\x1d\n\nrekey_time\x18\x1e \x01(\tR\trekeyTime\x12\x1f\n\x0breauth_time\x18\x1f \x01(\tR\nreauthTime\x12\x1d\n\nlocal_vips\x18  \x03(\tR\tlocalVips\x12\x1f\n\x0bremote_vips\x18! \x03(\tR\nremoteVips\x12!\n\x0ctasks_queued\x18\" \x03(\tR\x0btasksQueued\x12!\n\x0ctasks_active\x18# \x03(\tR\x0btasksActive\x12#\n\rtasks_passive\x18$ \x03(\tR\x0ctasksPassive\x12<\n\x08\x63hildsas\x18% \x03(\x0b\x32 .opi_api.security.v1.ListChildSaR\x08\x63hildsas\"N\n\x14IPsecListSasResponse\x12\x36\n\x06ikesas\x18\x01 \x03(\x0b\x32\x1e.opi_api.security.v1.ListIkeSaR\x06ikesas\")\n\x15IPsecListConnsRequest\x12\x10\n\x03ike\x18\x01 \x01(\tR\x03ike\"\xdf\x03\n\x0cListConnAuth\x12\x14\n\x05\x63lass\x18\x01 \x01(\tR\x05\x63lass\x12\x18\n\x07\x65\x61ptype\x18\x02 \x01(\tR\x07\x65\x61ptype\x12\x1c\n\teapvendor\x18\x03 \x01(\tR\teapvendor\x12\x14\n\x05xauth\x18\x04 \x01(\tR\x05xauth\x12\x1e\n\nrevocation\x18\x05 \x01(\tR\nrevocation\x12\x0e\n\x02id\x18\x06 \x01(\tR\x02id\x12\x13\n\x05\x63\x61_id\x18\x07 \x01(\tR\x04\x63\x61Id\x12\x15\n\x06\x61\x61\x61_id\x18\x08 \x01(\tR\x05\x61\x61\x61Id\x12\x15\n\x06\x65\x61p_id\x18\t \x01(\tR\x05\x65\x61pId\x12\x19\n\x08xauth_id\x18\n \x01(\tR\x07xauthId\x12\x31\n\x05group\x18\x0b \x01(\x0b\x32\x1b.opi_api.security.v1.GroupsR\x05group\x12@\n\x0b\x63\x65rt_policy\x18\x0c \x01(\x0b\x32\x1f.opi_api.security.v1.CertPolicyR\ncertPolicy\x12\x30\n\x05\x63\x65rts\x18\r \x01(\x0b\x32\x1a.opi_api.security.v1.CertsR\x05\x63\x65rts\x12\x36\n\x07\x63\x61\x63\x65rts\x18\x0e \x01(\x0b\x32\x1c.opi_api.security.v1.CaCertsR\x07\x63\x61\x63\x65rts\"\xb0\x03\n\tListChild\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x12\n\x04mode\x18\x02 \x01(\tR\x04mode\x12\x14\n\x05label\x18\x03 \x01(\tR\x05label\x12\x1d\n\nrekey_time\x18\x04 \x01(\rR\trekeyTime\x12\x1f\n\x0brekey_bytes\x18\x05 \x01(\rR\nrekeyBytes\x12#\n\rrekey_packets\x18\x06 \x01(\rR\x0crekeyPackets\x12\x1d\n\ndpd_action\x18\x07 \x01(\tR\tdpdAction\x12!\n\x0c\x63lose_action\x18\x08 \x01(\tR\x0b\x63loseAction\x12@\n\x08local_ts\x18\t \x01(\x0b\x32%.opi_api.security.v1.TrafficSelectorsR\x07localTs\x12\x42\n\tremote_ts\x18\n \x01(\x0b\x32%.opi_api.security.v1.TrafficSelectorsR\x08remoteTs\x12\x1c\n\tinterface\x18\x0b \x01(\tR\tinterface\x12\x1a\n\x08priority\x18\x0c \x01(\tR\x08priority\"\xc5\x04\n\x0cListConnResp\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12;\n\x0blocal_addrs\x18\x02 \x03(\x0b\x32\x1a.opi_api.security.v1.AddrsR\nlocalAddrs\x12=\n\x0cremote_addrs\x18\x03 \x03(\x0b\x32\x1a.opi_api.security.v1.AddrsR\x0bremoteAddrs\x12\x18\n\x07version\x18\x04 \x01(\tR\x07version\x12\x1f\n\x0breauth_time\x18\x05 \x01(\rR\nreauthTime\x12\x1d\n\nrekey_time\x18\x06 \x01(\rR\trekeyTime\x12\x16\n\x06unique\x18\x07 \x01(\tR\x06unique\x12\x1b\n\tdpd_delay\x18\x08 \x01(\rR\x08\x64pdDelay\x12\x1f\n\x0b\x64pd_timeout\x18\t \x01(\rR\ndpdTimeout\x12\x10\n\x03ppk\x18\n \x01(\tR\x03ppk\x12!\n\x0cppk_required\x18\x0b \x01(\tR\x0bppkRequired\x12@\n\nlocal_auth\x18\x0c \x03(\x0b\x32!.opi_api.security.v1.ListConnAuthR\tlocalAuth\x12\x42\n\x0bremote_auth\x18\r \x03(\x0b\x32!.opi_api.security.v1.ListConnAuthR\nremoteAuth\x12:\n\x08\x63hildren\x18\x0e \x03(\x0b\x32\x1e.opi_api.security.v1.ListChildR\x08\x63hildren\"[\n\x16IPsecListConnsResponse\x12\x41\n\nconnection\x18\x01 \x03(\x0b\x32!.opi_api.security.v1.ListConnRespR\nconnection\"Y\n\x15IPsecListCertsRequest\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x12\n\x04\x66lag\x18\x02 \x01(\tR\x04\x66lag\x12\x18\n\x07subject\x18\x03 \x01(\tR\x07subject\"\x8a\x02\n\x08ListCert\x12\x38\n\x04type\x18\x01 \x01(\x0e\x32$.opi_api.security.v1.CertificateTypeR\x04type\x12<\n\x04\x66lag\x18\x02 \x01(\x0e\x32(.opi_api.security.v1.X509CertificateFlagR\x04\x66lag\x12\x1e\n\nhasprivkey\x18\x03 \x01(\tR\nhasprivkey\x12\x12\n\x04\x64\x61ta\x18\x04 \x01(\tR\x04\x64\x61ta\x12\x18\n\x07subject\x18\x05 \x01(\tR\x07subject\x12\x1c\n\tnotbefore\x18\x06 \x01(\tR\tnotbefore\x12\x1a\n\x08notafter\x18\x07 \x01(\tR\x08notafter\"M\n\x16IPsecListCertsResponse\x12\x33\n\x05\x63\x65rts\x18\x01 \x03(\x0b\x32\x1d.opi_api.security.v1.ListCertR\x05\x63\x65rts\"W\n\x14IPsecLoadConnRequest\x12?\n\nconnection\x18\x01 \x01(\x0b\x32\x1f.opi_api.security.v1.ConnectionR\nconnection\"1\n\x15IPsecLoadConnResponse\x12\x18\n\x07success\x18\x01 \x01(\tR\x07success\",\n\x16IPsecUnloadConnRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\"3\n\x17IPsecUnloadConnResponse\x12\x18\n\x07success\x18\x01 \x01(\tR\x07success*\x92\x02\n\x0f\x43ryptoAlgorithm\x12 \n\x1c\x43RYPTO_ALGORITHM_UNSPECIFIED\x10\x00\x12\x1b\n\x17\x43RYPTO_ALGORITHM_AES128\x10\x01\x12\x1b\n\x17\x43RYPTO_ALGORITHM_AES192\x10\x02\x12\x1b\n\x17\x43RYPTO_ALGORITHM_AES256\x10\x03\x12!\n\x1d\x43RYPTO_ALGORITHM_AES128GCM128\x10\x04\x12!\n\x1d\x43RYPTO_ALGORITHM_AES256GCM128\x10\x05\x12\x1f\n\x1b\x43RYPTO_ALGORITHM_AES128GMAC\x10\x06\x12\x1f\n\x1b\x43RYPTO_ALGORITHM_AES256GMAC\x10\x07*\x92\x02\n\x0eIntegAlgorithm\x12\x1f\n\x1bINTEG_ALGORITHM_UNSPECIFIED\x10\x00\x12\x17\n\x13INTEG_ALGORITHM_MD5\x10\x01\x12\x1b\n\x17INTEG_ALGORITHM_MD5_128\x10\x02\x12\x18\n\x14INTEG_ALGORITHM_SHA1\x10\x03\x12\x1c\n\x18INTEG_ALGORITHM_SHA1_160\x10\x04\x12\x1a\n\x16INTEG_ALGORITHM_SHA256\x10\x05\x12\x1a\n\x16INTEG_ALGORITHM_SHA384\x10\x07\x12\x1a\n\x16INTEG_ALGORITHM_SHA512\x10\x08\x12\x1d\n\x19INTEG_ALGORITHM_SHA256_96\x10\t*\xd2\x02\n\x08\x44HGroups\x12\x19\n\x15\x44H_GROUPS_UNSPECIFIED\x10\x00\x12\x15\n\x11\x44H_GROUPS_MODP768\x10\x01\x12\x16\n\x12\x44H_GROUPS_MODP1024\x10\x02\x12\x16\n\x12\x44H_GROUPS_MODP1536\x10\x03\x12\x16\n\x12\x44H_GROUPS_MODP2048\x10\x04\x12\x16\n\x12\x44H_GROUPS_MODP3072\x10\x05\x12\x16\n\x12\x44H_GROUPS_MODP4096\x10\x06\x12\x16\n\x12\x44H_GROUPS_MODP6144\x10\x07\x12\x16\n\x12\x44H_GROUPS_MODP8192\x10\x08\x12\x1a\n\x16\x44H_GROUPS_MODP1024S160\x10\t\x12\x1a\n\x16\x44H_GROUPS_MODP2048S224\x10\n\x12\x1a\n\x16\x44H_GROUPS_MODP2048S256\x10\x0b\x12\x18\n\x14\x44H_GROUPS_CURVE25519\x10\x0c*\xce\x01\n\nPRFunction\x12\x1b\n\x17PR_FUNCTION_UNSPECIFIED\x10\x00\x12\x13\n\x0fPR_FUNCTION_MD5\x10\x01\x12\x14\n\x10PR_FUNCTION_SHA1\x10\x02\x12\x17\n\x13PR_FUNCTION_AESXCBC\x10\x03\x12\x17\n\x13PR_FUNCTION_AESCMAC\x10\x04\x12\x16\n\x12PR_FUNCTION_SHA256\x10\x05\x12\x16\n\x12PR_FUNCTION_SHA384\x10\x06\x12\x16\n\x12PR_FUNCTION_SHA512\x10\x07*b\n\tIpsecMode\x12\x1a\n\x16IPSEC_MODE_UNSPECIFIED\x10\x00\x12\x1a\n\x16IPSEC_MODE_TUNNEL_MODE\x10\x01\x12\x1d\n\x19IPSEC_MODE_TRANSPORT_MODE\x10\x02*v\n\x08\x41uthType\x12\x19\n\x15\x41UTH_TYPE_UNSPECIFIED\x10\x00\x12\x14\n\x10\x41UTH_TYPE_PUBKEY\x10\x01\x12\x11\n\rAUTH_TYPE_PSK\x10\x02\x12\x13\n\x0f\x41UTH_TYPE_XAUTH\x10\x03\x12\x11\n\rAUTH_TYPE_EAP\x10\x04*\x86\x02\n\nIkeSaState\x12\x1c\n\x18IKE_SA_STATE_UNSPECIFIED\x10\x00\x12\x18\n\x14IKE_SA_STATE_CREATED\x10\x01\x12\x1b\n\x17IKE_SA_STATE_CONNECTING\x10\x02\x12\x1c\n\x18IKE_SA_STATE_ESTABLISHED\x10\x03\x12\x18\n\x14IKE_SA_STATE_PASSIVE\x10\x04\x12\x19\n\x15IKE_SA_STATE_REKEYING\x10\x05\x12\x18\n\x14IKE_SA_STATE_REKEYED\x10\x06\x12\x19\n\x15IKE_SA_STATE_DELETING\x10\x07\x12\x1b\n\x17IKE_SA_STATE_DESTROYING\x10\x08*\xed\x02\n\x0c\x43hildSaState\x12\x1e\n\x1a\x43HILD_SA_STATE_UNSPECIFIED\x10\x00\x12\x1a\n\x16\x43HILD_SA_STATE_CREATED\x10\x01\x12\x19\n\x15\x43HILD_SA_STATE_ROUTED\x10\x02\x12\x1d\n\x19\x43HILD_SA_STATE_INSTALLING\x10\x03\x12\x1c\n\x18\x43HILD_SA_STATE_INSTALLED\x10\x04\x12\x1b\n\x17\x43HILD_SA_STATE_UPDATING\x10\x05\x12\x1b\n\x17\x43HILD_SA_STATE_REKEYING\x10\x06\x12\x1a\n\x16\x43HILD_SA_STATE_REKEYED\x10\x07\x12\x1b\n\x17\x43HILD_SA_STATE_RETRYING\x10\x08\x12\x1b\n\x17\x43HILD_SA_STATE_DELETING\x10\t\x12\x1a\n\x16\x43HILD_SA_STATE_DELETED\x10\n\x12\x1d\n\x19\x43HILD_SA_STATE_DESTROYING\x10\x0b*\xb6\x01\n\x0f\x43\x65rtificateType\x12%\n!CERTIFICATE_TYPE_X509_UNSPECIFIED\x10\x00\x12\x1c\n\x18\x43\x45RTIFICATE_TYPE_X509_AC\x10\x01\x12\x1d\n\x19\x43\x45RTIFICATE_TYPE_X509_CRL\x10\x02\x12\"\n\x1e\x43\x45RTIFICATE_TYPE_OCSP_RESPONSE\x10\x03\x12\x1b\n\x17\x43\x45RTIFICATE_TYPE_PUBKEY\x10\x04*\x98\x01\n\x13X509CertificateFlag\x12%\n!X509_CERTIFICATE_FLAG_UNSPECIFIED\x10\x00\x12\x1c\n\x18X509_CERTIFICATE_FLAG_CA\x10\x01\x12\x1c\n\x18X509_CERTIFICATE_FLAG_AA\x10\x02\x12\x1e\n\x1aX509_CERTIFICATE_FLAG_OCSP\x10\x03\x32\xa9\x08\n\x0cIPsecService\x12\x65\n\x0cIPsecVersion\x12(.opi_api.security.v1.IPsecVersionRequest\x1a).opi_api.security.v1.IPsecVersionResponse\"\x00\x12_\n\nIPsecStats\x12&.opi_api.security.v1.IPsecStatsRequest\x1a\'.opi_api.security.v1.IPsecStatsResponse\"\x00\x12h\n\rIPsecInitiate\x12).opi_api.security.v1.IPsecInitiateRequest\x1a*.opi_api.security.v1.IPsecInitiateResponse\"\x00\x12k\n\x0eIPsecTerminate\x12*.opi_api.security.v1.IPsecTerminateRequest\x1a+.opi_api.security.v1.IPsecTerminateResponse\"\x00\x12_\n\nIPsecRekey\x12&.opi_api.security.v1.IPsecRekeyRequest\x1a\'.opi_api.security.v1.IPsecRekeyResponse\"\x00\x12\x65\n\x0cIPsecListSas\x12(.opi_api.security.v1.IPsecListSasRequest\x1a).opi_api.security.v1.IPsecListSasResponse\"\x00\x12k\n\x0eIPsecListConns\x12*.opi_api.security.v1.IPsecListConnsRequest\x1a+.opi_api.security.v1.IPsecListConnsResponse\"\x00\x12k\n\x0eIPsecListCerts\x12*.opi_api.security.v1.IPsecListCertsRequest\x1a+.opi_api.security.v1.IPsecListCertsResponse\"\x00\x12h\n\rIPsecLoadConn\x12).opi_api.security.v1.IPsecLoadConnRequest\x1a*.opi_api.security.v1.IPsecLoadConnResponse\"\x00\x12n\n\x0fIPsecUnloadConn\x12+.opi_api.security.v1.IPsecUnloadConnRequest\x1a,.opi_api.security.v1.IPsecUnloadConnResponse\"\x00\x42\x32Z0github.com/opiproject/opi-api/security/v1/gen/gob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ipsec_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/opiproject/opi-api/security/v1/gen/go'
  _globals['_CRYPTOALGORITHM']._serialized_start=7959
  _globals['_CRYPTOALGORITHM']._serialized_end=8233
  _globals['_INTEGALGORITHM']._serialized_start=8236
  _globals['_INTEGALGORITHM']._serialized_end=8510
  _globals['_DHGROUPS']._serialized_start=8513
  _globals['_DHGROUPS']._serialized_end=8851
  _globals['_PRFUNCTION']._serialized_start=8854
  _globals['_PRFUNCTION']._serialized_end=9060
  _globals['_IPSECMODE']._serialized_start=9062
  _globals['_IPSECMODE']._serialized_end=9160
  _globals['_AUTHTYPE']._serialized_start=9162
  _globals['_AUTHTYPE']._serialized_end=9280
  _globals['_IKESASTATE']._serialized_start=9283
  _globals['_IKESASTATE']._serialized_end=9545
  _globals['_CHILDSASTATE']._serialized_start=9548
  _globals['_CHILDSASTATE']._serialized_end=9913
  _globals['_CERTIFICATETYPE']._serialized_start=9916
  _globals['_CERTIFICATETYPE']._serialized_end=10098
  _globals['_X509CERTIFICATEFLAG']._serialized_start=10101
  _globals['_X509CERTIFICATEFLAG']._serialized_end=10253
  _globals['_PROPOSALS']._serialized_start=37
  _globals['_PROPOSALS']._serialized_end=293
  _globals['_VIPS']._serialized_start=295
  _globals['_VIPS']._serialized_end=319
  _globals['_POOLS']._serialized_start=321
  _globals['_POOLS']._serialized_end=348
  _globals['_CERTS']._serialized_start=350
  _globals['_CERTS']._serialized_end=377
  _globals['_PUBKEYS']._serialized_start=379
  _globals['_PUBKEYS']._serialized_end=412
  _globals['_GROUPS']._serialized_start=414
  _globals['_GROUPS']._serialized_end=444
  _globals['_CERTPOLICY']._serialized_start=446
  _globals['_CERTPOLICY']._serialized_end=491
  _globals['_CACERTS']._serialized_start=493
  _globals['_CACERTS']._serialized_end=526
  _globals['_LOCALAUTH']._serialized_start=529
  _globals['_LOCALAUTH']._serialized_end=786
  _globals['_REMOTEAUTH']._serialized_start=789
  _globals['_REMOTEAUTH']._serialized_end=1173
  _globals['_TRAFFICSELECTORS']._serialized_start=1176
  _globals['_TRAFFICSELECTORS']._serialized_end=1346
  _globals['_TRAFFICSELECTORS_TRAFFICSELECTOR']._serialized_start=1267
  _globals['_TRAFFICSELECTORS_TRAFFICSELECTOR']._serialized_end=1346
  _globals['_ADDRS']._serialized_start=1348
  _globals['_ADDRS']._serialized_end=1375
  _globals['_CHILD']._serialized_start=1378
  _globals['_CHILD']._serialized_end=1999
  _globals['_CONNECTION']._serialized_start=2002
  _globals['_CONNECTION']._serialized_end=2784
  _globals['_IPSECVERSIONREQUEST']._serialized_start=2786
  _globals['_IPSECVERSIONREQUEST']._serialized_end=2807
  _globals['_IPSECVERSIONRESPONSE']._serialized_start=2810
  _globals['_IPSECVERSIONRESPONSE']._serialized_end=2960
  _globals['_IPSECSTATSREQUEST']._serialized_start=2962
  _globals['_IPSECSTATSREQUEST']._serialized_end=2981
  _globals['_IPSECSTATSRESPONSE']._serialized_start=2983
  _globals['_IPSECSTATSRESPONSE']._serialized_end=3027
  _globals['_IPSECINITIATEREQUEST']._serialized_start=3029
  _globals['_IPSECINITIATEREQUEST']._serialized_end=3145
  _globals['_IPSECINITIATERESPONSE']._serialized_start=3147
  _globals['_IPSECINITIATERESPONSE']._serialized_end=3170
  _globals['_IPSECTERMINATEREQUEST']._serialized_start=3173
  _globals['_IPSECTERMINATEREQUEST']._serialized_end=3362
  _globals['_IPSECTERMINATERESPONSE']._serialized_start=3364
  _globals['_IPSECTERMINATERESPONSE']._serialized_end=3472
  _globals['_IPSECREKEYREQUEST']._serialized_start=3475
  _globals['_IPSECREKEYREQUEST']._serialized_end=3608
  _globals['_IPSECREKEYRESPONSE']._serialized_start=3610
  _globals['_IPSECREKEYRESPONSE']._serialized_end=3682
  _globals['_IPSECLISTSASREQUEST']._serialized_start=3685
  _globals['_IPSECLISTSASREQUEST']._serialized_end=3822
  _globals['_LISTCHILDSA']._serialized_start=3825
  _globals['_LISTCHILDSA']._serialized_end=4353
  _globals['_LISTIKESA']._serialized_start=4356
  _globals['_LISTIKESA']._serialized_end=5561
  _globals['_IPSECLISTSASRESPONSE']._serialized_start=5563
  _globals['_IPSECLISTSASRESPONSE']._serialized_end=5641
  _globals['_IPSECLISTCONNSREQUEST']._serialized_start=5643
  _globals['_IPSECLISTCONNSREQUEST']._serialized_end=5684
  _globals['_LISTCONNAUTH']._serialized_start=5687
  _globals['_LISTCONNAUTH']._serialized_end=6166
  _globals['_LISTCHILD']._serialized_start=6169
  _globals['_LISTCHILD']._serialized_end=6601
  _globals['_LISTCONNRESP']._serialized_start=6604
  _globals['_LISTCONNRESP']._serialized_end=7185
  _globals['_IPSECLISTCONNSRESPONSE']._serialized_start=7187
  _globals['_IPSECLISTCONNSRESPONSE']._serialized_end=7278
  _globals['_IPSECLISTCERTSREQUEST']._serialized_start=7280
  _globals['_IPSECLISTCERTSREQUEST']._serialized_end=7369
  _globals['_LISTCERT']._serialized_start=7372
  _globals['_LISTCERT']._serialized_end=7638
  _globals['_IPSECLISTCERTSRESPONSE']._serialized_start=7640
  _globals['_IPSECLISTCERTSRESPONSE']._serialized_end=7717
  _globals['_IPSECLOADCONNREQUEST']._serialized_start=7719
  _globals['_IPSECLOADCONNREQUEST']._serialized_end=7806
  _globals['_IPSECLOADCONNRESPONSE']._serialized_start=7808
  _globals['_IPSECLOADCONNRESPONSE']._serialized_end=7857
  _globals['_IPSECUNLOADCONNREQUEST']._serialized_start=7859
  _globals['_IPSECUNLOADCONNREQUEST']._serialized_end=7903
  _globals['_IPSECUNLOADCONNRESPONSE']._serialized_start=7905
  _globals['_IPSECUNLOADCONNRESPONSE']._serialized_end=7956
  _globals['_IPSECSERVICE']._serialized_start=10256
  _globals['_IPSECSERVICE']._serialized_end=11321
# @@protoc_insertion_point(module_scope)