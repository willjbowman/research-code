clear all
w = logspace(-1,6,100); %gamry max is 1MH

%IS sample information - s = 1/r = L/RA (S/cm)
L = 1.2; %cm - sample thickness
A = 0.007853982; %cm^2 - sample area
%Tc = [100:50:800]; %C - sample temperature
%Tk = Tc+273; %K - sample temperature

R_int_400 = 793.5; %ohm
R_gb_400 = 1.426e5; %ohm

rho_int_400 = R_int_400*.914/.076533; %ohm-cm
rho_gb_400 = R_gb_400*.914/.076533; %ohm-cm

R0 = 368.3; %ohm - system 'offset' resistance
R1 = 5.09e3; %ohm - R1 resistance
R2 = 8.01e3; %ohm - R2 resistance
%R3 = 5e2; %ohm - R3 resistance
Y1 = 1.00E-09; %F - C1 capacitance
Y2 = 9.74e-6; %F - C2 capacitance
%Y3 = 0; %F - C3 capacitance
a1 = .872; %
a2 = .54; %
%a3 = 0; %

%C1 = 4.1e-7; %F - C1 capacitance
%C2 = 1.2e-8; %F - C2 capacitance
%C3 = 20e-6; %F - C3 capacitance

%Z_RQ = R1./(1+w.^2*R1^2*C1^2)-(1i.*w*R1^2*C1)./(1+w.^2*R1^2*C1^2); %|| R-C Impedance
%Z_RQreal = real(Z_RQ); %Real impedance component
%Z_RQimg = imag(Z_RQ); %Imaginary impedance component

%Z_RRQ = R0 + R1./(1+w.^2*R1^2*C1^2)-(1i.*w*R1^2*C1)./(1+w.^2*R1^2*C1^2); %|| R-C Impedance
%Z_RRQreal = real(Z_RRQ); %Real impedance component
%Z_RRQimg = imag(Z_RRQ); %Imaginary impedance component
%%%%%%%%%%%%%%
ZA = 1./(1/R2+Y2.*(1i.*w).^a2);
ZB = 1./(1/R1+Y1.*(1i.*w).^a1);

Z_RRQRQ = R0 + ZA + ZB;
Z_RRQRQreal = real(Z_RRQRQ);
Z_RRQRQimg = imag(Z_RRQRQ);
%%%%%%%%%%%%%%
%Z_RRQRQRQ = R0 + 1./(1/R1+1i.*w*C1) + 1./(1/R2+1i.*w*C2) + 1./(1/R3+1i.*w*C3);
%Z_RRQRQRQreal = real(Z_RRQRQRQ);
%Z_RRQRQRQimg = imag(Z_RRQRQRQ);


figure(1)
%plot(Z_RQreal,-Z_RQimg,'s',Z_RRQreal,-Z_RRQimg,'o',Z_RRQRQreal,-Z_RRQRQimg,'*',Z_RRQRQRQreal,-Z_RRQRQRQimg,'v');
plot(Z_RRQRQreal,-Z_RRQRQimg,'-')
%legend('R_1--C','R_0--R_1C','R_0--R_1C_1--R_2C_2','R_0--R_1C_1--R_2C_2--R_3C_3','SouthWest');
%title('R_0 = 10\Omega, R_1 = 100\Omega, C_1 = 2\muF, R_2 = 200\Omega, C_2 = 2\muF');
%axis('equal')
axis([0 R0+R1+R2 0 R0+R1+R2])

%figure(2)
%plot(Z_RQreal,-Z_RQimg,'s',Z_RRQreal,-Z_RRQimg,'o',Z_RRQRQreal,-Z_RRQRQimg,'*',Z_RRQRQRQreal,-Z_RRQRQRQimg,'v');
%plot(Z_RRQRQreal,-Z_RRQRQimg)
%legend('R_1--C','R_0--R_1C','R_0--R_1C_1--R_2C_2','R_0--R_1C_1--R_2C_2--R_3C_3','SouthWest');
%title('R_0 = 10\Omega, R_1 = 100\Omega, C_1 = 2\muF, R_2 = 200\Omega, C_2 = 2\muF');
%axis('equal')
%axis([0 2000 0 2000])

%Rtot = R1 + R2; %ohm - Total resistance
%Rint = R1; %ohm - grain interior resistance
%Rgb = R2; %ohm - grain boundary resistance
%Cint = C1; %F - grain interior capacitance 
%Cgb = C2; %F - gring boundary capacitance

%Stot = L/(Rtot*A); %S/m - total sample ionic conductivity
%Sint = L/(Rint*A); %S/m - grain interior ionic conductivity
%Sgb = Sint*(Rint*Cint/(Rgb*Cgb)); %S/m - grain boundary ionic conductivity