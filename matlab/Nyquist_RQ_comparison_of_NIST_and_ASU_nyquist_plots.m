w = [1:1e2:10e7]; %gamry max is 1MHz

%IS sample information - s = 1/r = L/RA (S/m)
L = .076533; %cm - sample thickness
d = 18e-3; %m - sample diameter
A = .914; %cm^2 - sample area
Tc = [100:50:800]; %C - sample temperature
Tk = Tc+273; %K - sample temperature

R0 = 0; %ohm - system 'offset' resistance
R1 = 8.92; %ohm - R1 resistance from asu 700 C (This is what I am calling R0 in the notes)
R2 = 80.2; %ohm - R2 resistance from asu 700 C (This is what I am calling R1 in the notes)
R3 = 431.9; %ohm - R3 resistance
Y1 = 3.04e-8; %F - C1 capacitance
Y2 = 3.04e-8; %F - C2 capacitance
Y3 = 5.67e-6; %F - C3 capacitance
a1 = .945; %
a2 = .945; %
a3 = 0.754; %

C1 = (R1.^(1-a1).*Y1).^(1./a1); %CPE capacitance
C2 = (R2.^(1-a2).*Y2).^(1./a2);
C3 = (R3.^(1-a3).*Y3).^(1./a3);

Z_RQ = R1./(1+w.^2*R1^2*C1^2)-(1i.*w*R1^2*C1)./(1+w.^2*R1^2*C1^2); %|| R-C Impedance
Z_RQreal = real(Z_RQ); %Real impedance component
Z_RQimg = imag(Z_RQ); %Imaginary impedance component

Z_RRQ = R0 + R1./(1+w.^2*R1^2*C1^2)-(1i.*w*R1^2*C1)./(1+w.^2*R1^2*C1^2); %|| R-C Impedance
Z_RRQreal = real(Z_RRQ); %Real impedance component
Z_RRQimg = imag(Z_RRQ); %Imaginary impedance component

Z_RRQRQ = R0 + 1./(1/R1+Y1.*(1i.*w).^a1) + 1./(1/R2+Y2.*(1i.*w).^a2);
Z_RRQRQreal = real(Z_RRQRQ);
Z_RRQRQimg = imag(Z_RRQRQ);

Z_RRQRQRQ = R0 + 1./(1/R1+Y1.*(1i.*w).^a1) + 1./(1/R2+Y2.*(1i.*w).^a2) + 1./(1/R3+Y3.*(1i.*w).^a3);
Z_RRQRQRQreal = real(Z_RRQRQRQ);
Z_RRQRQRQimg = imag(Z_RRQRQRQ);


figure(1)
%plot(Z_RQreal,-Z_RQimg,'s',Z_RRQreal,-Z_RRQimg,'o',Z_RRQRQreal,-Z_RRQRQimg,'*',Z_RRQRQRQreal,-Z_RRQRQRQimg,'v');
plot(Z_RRQRQRQreal,-Z_RRQRQRQimg,'-')
%legend('R_1--C','R_0--R_1C','R_0--R_1C_1--R_2C_2','R_0--R_1C_1--R_2C_2--R_3C_3','SouthWest');
%title('R_0 = 10\Omega, R_1 = 100\Omega, C_1 = 2\muF, R_2 = 200\Omega, C_2 = 2\muF');
%axis('equal')
axis([0 R0+R1+R2+R3 0 R0+R1+R2+R3])

Rtot = R1 + R2; %ohm - Total resistance
Rint = R1; %ohm - grain interior resistance
Rgb = R2; %ohm - grain boundary resistance
Cint = C1; %F - grain interior capacitance 
Cgb = C2; %F - gring boundary capacitance

Stot = L/(Rtot*A); %S/m - total sample ionic conductivity
Sint = L/(Rint*A); %S/m - grain interior ionic conductivity
Sgb = Sint*(Rint*Cint/(Rgb*Cgb)); %S/m - grain boundary ionic conductivity