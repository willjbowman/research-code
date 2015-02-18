clear all; clf;
w = logspace(-1,16.8,100); %gamry max is 1MH, but there is some fudge factor so 10^6.8 in matlab is about the same
Ai = .914; ti = .077;
Cinti = 4.07e-11; Cgbi = 1.17e-8;
Rinti = 793.5; Rgbi = 1.43e5;

cint = Cinti/(Ai/ti); cgb = Cgbi/(Ai/ti);
rint = Rinti*(Ai/ti); rgb = Rgbi*(Ai/ti);

d = [1.3 1.0 0.7 0.4 0.1]; A = 3.14159.*d.^2/4;
t = [0.1 0.2 0.3 0.4 0.5];
fig = ['1.3' '1.0' '0.7' '0.4' '0.1'];
for i = 1%:length(t)
    for j = 1%:length(A)
        R0 = 00;
        R1 = rint*t(i)/A(j);
        R2 = rgb*t(i)/A(j);
        
        C1 = cint*A(j)/t(i);
        C2 = cgb*A(j)/t(i);
        
        ZA = 1./(1/R1+1i.*w*C1);
        ZB = 1./(1/R2+1i.*w*C2);
        
        Z_RRC = R0 + ZA + ZB;
        Z_RRCreal = real(Z_RRC);
        Z_RRCimg = imag(Z_RRC);
        
        figure(j)
        hold on
        plot(Z_RRCreal,-Z_RRCimg,'.')
        axis([0 R0+R1+R1/100 0 R0+R1+R1/100])
        title(d(j));
    end
end