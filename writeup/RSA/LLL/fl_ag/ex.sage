from Crypto.Util.number import long_to_bytes

N = 10552642384365129586491509600782945412337277857912016872204502743960245028115506632447849065284007668900072388051913143865262223101240686928487683568079554937298909563589070393050774335659305500634934817243567014388724714813303153240769377962577189329350484473273045864053642731651608363106120918977638930189836376254203882217624714513547709083420255134541972900460599384731283053739376462302868128559171026292354163149030712872651178876722691245045159379604057661199401000873801445353472363379029871645849172778371784272955440756825120912127334197628016607177884517007297868319440429716229612753535372733394086473279

R.<x> = PolynomialRing(Zmod(N))

e = 257
A_e = R(3177482343207874904907532376324442143117730245928501961718443711649032883938842863124771456408075887142069243160971142725532872565987268798278943270192700520341288988003431310085855468355218878114314894880299296507444422638379221697708598083809818067076980915614087187437109855415087003114727262140580647585967287172230203085106718195581239090580640300111219385383577869551936076421657366135374298264945010079888349437307284760866970781652332511218794217739333230323996362576623763436798333404764373229646410451368218037640285132297992104641844187349452135037725942544518015609727303409388799383579378273134155372937)
B_e = R(255471710041322901308975464760452116131534387637893001499697371668346323395039191194759437996725379980397012343125200220970390650940409107372948477547286190990740225495541306630719395392223710513099974239348696246850167294472493689411475138675281918345183054757365258601326937400353504456287981058057910560927375498422201402032576554731096939399425135527686153118977579014586151787957258349224667838875997154291378921457451142330897248340158660608614064313910430033734650303792004502107861857498298241671877798088339672854469842544780536571835803225725831810072713661160701407899175162400551856066373243530834524333)
C_e = R(4487347101729671066943449187407157166746146512096516031820084543231215765411184930117838870596554803416359764818648393699583261304855810883058008746203698462517148414775302286335932044796825411150267394368515850779643583034362935205702767103022818423951440243147870552683928972132797767456746417095772610896043471048940731728561063543595675316418849767594445677180598850151530903061335565656848938741461693335125228020624963783656050613669364474231438851307935565905464952201752579696548576035104052981441822249250489483179937724308750043843782665342986957163482275767548506737385746375344091003310532487923891282517)

f1, f2 = x^e - B_e//A_e, (256^34 + x)^e - C_e//A_e
while f2:
    f1, f2 = f2, f1%f2

M = matrix([[1, ZZ(-f1.monic()[0])], [0, ZZ(N)]])
M = M.LLL()

print(long_to_bytes(int(-M[0][0]))+long_to_bytes(int(-M[0][1])))