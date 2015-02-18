%What are we hoping to learn from this script?
%(1) the current passing through the micro eis specimen
%(2) the current passing through the TEM specimen
%(3) what is the best dimension for ex-situ films?
%
clear all
%GDC ASU experiment
A = 0.914 ; %cm eis specimen electrical contact area
L = 0.0765; %cm eis specimen thickness (electrode sepatation)
T = [700 650 600 550 500];
R = [80.01 433.3;187.9 1210;520.9 2731;1.38E+03	8.68E+03;5.21E+03 2.70E+04]; %ohm R1, R2 resistance
C = [1.43733E-08 1.42465E-08 1.46242E-08 1.38654E-08 1.35613E-08]; %F

%for temperatures from 700-500 C
rhoint = R(:,1)*A/L; %ohm-cm grain interior resistivity at various temperatures
%rhogb = R(:,2)*A/L; %ohm-cm grain boundary resistivity at various temperatures
%rhotot = (R(:,1)+R(:,2))*A/L; %ohm-cm total resistivity at various temperatures
cbar = C/A*L;
%new sample resistivity assuming differenent geometry and 
%same electrolyte resistivity
ax = (1e-4:1e-4:5e-4); %cm new specimen contact face width: 1 um - 10 um
a = ax.^2; %cm^2 new specimen contact area
l = 5e-4; %cm new specimen thickness
v = 20e-3; %V
lengthname = ['1' '2' '3' '4' '5' '6' '7' '8' '9' '10'];
marker = ['p' 'o' '*' '.' 'x' 's' 'd' '^' '<' '>'];
color = ['r' 'k' 'b' 'g' 'y'];
figure(1)
for t = 1:length(T)
    for edge = 1:length(a)
        iint(t,edge) = v*a(edge)/(rhoint(t)*l); %ohm new specimen grain interior resistance
    end
    plot(ax*10^4,iint(t,:),marker(t),'MarkerSize',8)
    hold on
end
legend('700','650','600','550','500','Location','NorthWest')
title('DC, 5 \mum, 20 mV excitation')
xlabel('contact edge length (\mum)'), ylabel('Current (A)')

%what is the frequency required to induce a current response > detection
%limit?
figure(2)

w = (1:100:1e6); %input frequency
for t = 1:length(T) %for area of 25um^2 and thickness 5um and 20mV
Z_500 = (1i.*w*cbar(t)*25e-8/l+1./(rhoint(t)*l/25e-8)).^-1; %Impedance as function of w for RC model
RR = real(Z_500); XX = imag(Z_500); %
i_500 = v.*cos(atan(XX./RR))./RR;
i_500_sin = v.*sin(atan(XX./RR))./XX;

plot(w,i_500,color(t),w,i_500_sin,'-',w,50e-9); %axis([0 1e3 0 1e-7])
title('Response I (A) vs. Excit. Volt. \omega [5 \mum cube, 20 mV]')
hold on
end
legend('700','650','600','550','500','Location','NorthWest')

figure(3)
plot(RR,-XX);
%rgb = rhogb(1)*l./a; %ohm new specimen grain boundary resistance
%rtot = rhotot(1)*l./a; %ohm new specimen total resistance

%I = V/R = V*A/(rho*L)
%Gamry voltage range (from webpage): 4.03 uV - 2.11 V

%iint = v./rint; %A grain interior current
%igb = v./rgb; %A grain boundary current
%itot = v./rtot; %A total specimen current

%figure(1)
%plot(ax/1e-4,iint,'x') %,ax/1e-4,igb,'o',ax/1e-4,itot,'*')
%legend('int','gb','tot'); title('current vs. electrical contact geometry 700C')
%xlabel('electrical contact edge length (um). i.e. sqrt(area)')
%ylabel('current (A)')

%Using the specific grain boundary argument
vv = 20e-3; %V
LL = (1e-6:1e-6:10e-6);
edge = (1e-6:1e-6:10e-6);
aa = edge.^2;
rho_gb500 = 322089e-2; %ohm-m (500C)
rho_int500 = 62196e-2; %ohm-m (500C)
lengthname = ['1' '2' '3' '4' '5' '6' '7' '8' '9' '10'];
marker = ['+' 'o' '*' '.' 'x' 's' 'd' '^' '<' '>'];

figure(4)
for i = 1:length(LL)
    for j = 1:length(edge)
        R_gb500 = rho_gb500.*LL(i)./aa(j);
        R_int500 = rho_int500.*LL(i)./aa(j);
        ii(i,j) = vv./(R_gb500+R_int500); %varying area for each length
    end
        plot(edge,ii(i,:),marker(i))
        
        hold on
end
xlabel('edge length m'); ylabel('current A'); 
title('20mV, specimen thickness increases from 1 um to 10 um')
legend('1','2','3','4','5','6','7','8','9','10','Location','NorthWest')