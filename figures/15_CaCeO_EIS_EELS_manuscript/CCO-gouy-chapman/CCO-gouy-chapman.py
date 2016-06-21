# dPhi = array of possible dPhi values
# x = array x values
# for.each dPhi:
# 	for.each x:
# 		solve profile parameter
# 		Cratio_i[i] = solution to C(x)/Cbulk
# 	Cratio_i_all[j,:] = Cratio_i
# 	least_squares[j] = least_squares( Cratio_i, composition_profile )
# 

e, kb = 
z = 
T = 
dPhi =

pro_par = np.tanh( z * e * dPhi[i] / ( 4 * kb * T ) )
pro_par_num = 1 + pro_par * exp( -chi / lam )
pro_par_den = 1 - pro_par * exp( -chi / lam )
Cx_Cb[i] = ( pro_par_num / pro_par_den ) ** ( 2 * 	z )