clear all; clf;
w = logspace(-1,9,100); %gamry max is 1MH, but there is some fudge factor so 10^6.8 in matlab is about the same
Cinti = 4.07e-11; Cgbi = 1.17e-8;
Rinti = 793.5; Rgbi = 1.43e5;
      ZA = 1./(1/Rinti+1i.*w*Cinti);
        ZB = 1./(1/Rgbi+1i.*w*Cgbi);
        
        Z_RRC = R0 + ZA + ZB;
        Z_RRCreal = real(Z_RRC);
        Z_RRCimg = imag(Z_RRC);
      
        plot(Z_RRCreal,-Z_RRCimg,'.')
        axis([0 R1+R1/100 0 R1+R1/100])
        
