
% segregation_ceria_afe_chem, v. 1.1

% Grain boundary segregation in doped ceria, taking the segregated vacancy
% as occurring in a separate phase, and no preferential dopant segregation.

% Adaptive finite element solver.
% See line 64 for description of function inputs; line 42 for outputs.

% The routine generally works for cases where there is not phase separation
% (a miscibility gap).

% Copyright (c) 2015, David S. Mebane
%All rights reserved.

%Redistribution and use in source and binary forms, with or without
%modification, are permitted provided that the following conditions are
%met:

%1. Redistributions of source code must retain the above copyright notice,
%this list of conditions and the following disclaimer.

%2. Redistributions in binary form must reproduce the above copyright
%notice, this list of conditions and the following disclaimer in the
%documentation and/or other materials provided with the distribution.

%THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
%IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
%THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
%PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
%CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
%EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
%PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
%PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
%LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
%NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
%SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


function [y, v, phi, lamv, lambd, nodes, flag] = segregation_ceria_afe_chem(varargin)

% y: dopant site fraction profile
% v: vacancy site fraction profile
% phi: electrostatic potential profile
% lamv: Lagrange multiplier / bulk chemical potential of vacancies (times the anion site density)
% lambd: Lagrange multiplier / bulk chemical potential of dopant (times the cation site density)
% nodes: distances from interface corresponding to y, v, phi
% flag: 1 = success; 2 = failure

if nargin ~= 5
    disp('Error: bad argument list: (<temperature in Kelvin>, <bulk dopant site fraction>, <number of initial elements>/<initial guess vector>, <grain radius>/<vector of nodes>, <parameter file name>)')
    y=0;
    v=0;
    phi=0;
    lamv=0;
    lambd=0;
    nodes=0;
    flag = 0;
    return;
end

warning('off', 'MATLAB:nearlySingularMatrix');

% function inputs
T = varargin{1};                % Temperature, K
yd = varargin{2};               % bulk dopant site fraction
if (length(varargin{3}) == 1)
    N = varargin{3};            % number of initial interior nodes (try 10 or 100)
    L = varargin{4};            % grain radius, m
else
    x0 = varargin{3};           % an initial guess at the solution if one is available: a column vector [y; v; phi; lamv; lambd].  y and v are length N+2; phi is length N+1
    nodes = varargin{4};        % node values corresponding to x0: length N+2
end

% some physical parameters
eps0 = 8.85e-12;
F = 96485.0;
R = 8.314;
avnum = 6.022e23;

% material parameters
paramfile = varargin{5};
par = importdata(paramfile,' ',2);
no = par.data(1);       % surface site density for vacancies, mol/m^2 (NvGB)
fv = par.data(2);       % vacancy self-interaction, J/mol
fo = par.data(3);       % vacancy segregation energy, J/mol
fy = par.data(4);       % dopant self-interaction, J/mol
fyv = par.data(5);      % dopant-vacancy interaction, J/mol
cv = par.data(6);       % vacancy gradient energy coefficient, J/mol-m
cd = par.data(7);       % dopant gradient energy coefficient, J/mol-m
epsr = par.data(8);     % relative permittivity
latpar = par.data(9);   % lattice parameter, m

% cubic fluorite structure parameters
ny = 4/(avnum*latpar^3);    % cation site density, mol/m^3
nv = 2*ny;                  % anion site density, mol/m^3
nvv = 3*nv;                 % anion-anion next-nearest-neighbor bond density, mol/m^3
nyv = 8*ny;                 % anion-cation next-nearest-neighbor bond density, mol/m^3
nyy = 4*ny;                 % cation-cation next-nearest-neighbor bond density, mol/m^3

vd = yd/4;                  % bulk vacancy site fraction (assuming 3+ dopant)
% vd = yd/2;                  % bulk vacancy site fraction (assuming 2+ dopant)

if (length(varargin{4}) == 1)
    h = L*ones(N+1,1)/(N+1);
    nodes = 0:h(1):L;
    phi = zeros(N+1,1);
    y = yd*ones(N+2,1);
    v = y/4;
    lambd = -(2*nyy*fy*y(N+2) + nyv*fyv*v(N+2) + ny*R*T*log(y(N+2)/(1-y(N+2))));
    lamv = -(2*nvv*fv*v(N+2) + nyv*fyv*y(N+2) + nv*R*T*log(v(N+2)/(1-v(N+2))));
else
    N = length(nodes)-2;
    y = x0(1:N+2);
    v = x0(N+3:2*N+4);
    phi = x0(2*N+5:3*N+5);
    lamv = x0(3*N+6);
    lambd = x0(3*N+7);
    h = zeros(N+1,1);
    for i=1:N+1
        h(i) = nodes(i+1) - nodes(i);
    end
end

refnum = 1;
while (1)
    
    % Newton's method solver
    
    J = zeros(3*N+7);
    f = zeros(3*N+7,1);
    ftest = f;
    
    x = [y; v; phi; lamv; lambd];
    
    f(1) = cd*(y(1)/h(1) - y(2)/h(1)) + h(1)*(2*nyy*fy*y(1) + nyv*fyv*v(1) + ny*R*T*log(y(1)/(1-y(1))) - ny*F*phi(1) + lambd)/2;
    for i=2:N+1
        f(i) = cd*(-y(i-1)/h(i-1) + y(i)*(1/h(i-1) + 1/h(i)) - y(i+1)/h(i)) + (h(i-1) + h(i))*(2*nyy*fy*y(i) + nyv*fyv*v(i) + ny*R*T*log(y(i)/(1-y(i))) - ny*F*phi(i) + lambd)/2;
    end
    f(N+2) = cd*(-y(N+1)/h(N+1) + y(N+2)/h(N+1)) + h(N+1)*(2*nyy*fy*y(N+2) + nyv*fyv*v(N+2) + ny*R*T*log(y(N+2)/(1-y(N+2))) + lambd)/2;
    
    f(N+3) = cv*(v(1)/h(1) - v(2)/h(1)) + no*fo + h(1)*(2*nvv*fv*v(1) + nyv*fyv*y(1) + nv*R*T*log(v(1)/(1-v(1))) + nv*2*F*phi(1) + lamv)/2;
    for i=2:N+1
        f(N+2+i) = cv*(-v(i-1)/h(i-1) + v(i)*(1/h(i-1) + 1/h(i)) - v(i+1)/h(i)) + (h(i-1) + h(i))*(2*nvv*fv*v(i) + nyv*fyv*y(i) + nv*R*T*log(v(i)/(1-v(i))) + nv*2*F*phi(i) + lamv)/2;
    end
    f(2*N+4) = cv*(-v(N+1)/h(N+1) + v(N+2)/h(N+1)) + h(N+1)*(2*nvv*fv*v(N+2) + nyv*fyv*y(N+2) + nv*R*T*log(v(N+2)/(1-v(N+2))) + lamv)/2;
    
    f(2*N+5) = epsr*eps0*(-phi(1)/h(1) + phi(2)/h(1)) + h(1)*F*(2*nv*v(1) - ny*y(1))/2;
    for i=2:N
        f(2*N+4+i) = epsr*eps0*(phi(i-1)/h(i-1) - phi(i)*(1/h(i-1) + 1/h(i)) + phi(i+1)/h(i)) + (h(i-1) + h(i))*F*(2*nv*v(i) - ny*y(i))/2;
    end
    f(3*N+5) = epsr*eps0*(phi(N)/h(N) - phi(N+1)*(1/h(N) + 1/h(N+1))) + (h(N) + h(N+1))*F*(2*nv*v(N+1) - ny*y(N+1))/2;
    
    f(3*N+6) = (y(1) - yd)*h(1)/2;
    for i=2:N+1
        f(3*N+6) = f(3*N+6) + (y(i) - yd)*(h(i-1) + h(i))/2;
    end
    f(3*N+6) = f(3*N+6) + (y(N+2) - yd)*h(N+1)/2;
    
    f(3*N+7) = (v(1) - vd)*h(1)/2;
    for i=2:N+1
        f(3*N+7) = f(3*N+7) + (v(i) - vd)*(h(i-1) + h(i))/2;
    end
    f(3*N+7) = f(3*N+7) + (v(N+2) - vd)*h(N+1)/2;
    
    f0 = f;
    if refnum == 1
        nf0 = norm(f0)/length(f0);
    end
    nf = norm(f)/length(f);
    its = 0;
    while (nf/nf0 > 1e-6 && nf > h(N+1) && its < 1000)
        
        J(1,1) = cd/h(1) + h(1)*(2*nyy*fy + ny*R*T/(y(1)*(1 - y(1))))/2;
        J(1,2) = -cd/h(1);
        J(1,N+3) = h(1)*nyv*fyv/2;
        J(1,2*N+5) = -h(1)*ny*F/2;
        J(1,3*N+7) = h(1)/2;
        for i=2:N+1
            J(i,i) = cd*(1/h(i-1) + 1/h(i)) + (h(i-1) + h(i))*(2*nyy*fy + ny*R*T/(y(i)*(1 - y(i))))/2;
            J(i,i+1) = -cd/h(i);
            J(i,i-1) = -cd/h(i-1);
            
            J(i,i+N+2) = (h(i-1) + h(i))*nyv*fyv/2;
            J(i,i+2*N+4) = -(h(i-1) + h(i))*ny*F/2;
            J(i,3*N+7) = (h(i-1) + h(i))/2;
        end
        J(N+2,N+2) = cd/h(N+1) + h(N+1)*(2*nyy*fy + ny*R*T/(y(N+2)*(1 - y(N+2))))/2;
        J(N+2,N+1) = -cd/h(N+1);
        J(N+2,2*N+4) = h(N+1)*nyv*fyv/2;
        J(N+2,3*N+7) = h(N+1)/2;
        
        J(N+3,N+3) = cv/h(1) + h(1)*(2*nvv*fv + nv*R*T/(v(1)*(1 - v(1))))/2;
        J(N+3,N+4) = -cv/h(1);
        J(N+3,1) = h(1)*nyv*fyv/2;
        J(N+3,2*N+5) = h(1)*2*nv*F/2;
        J(N+3,3*N+6) = h(1)/2;
        for i=2:N+1
            J(i+N+2,i+N+2) = cv*(1/h(i-1) + 1/h(i)) + (h(i-1) + h(i))*(2*nvv*fv + nv*R*T/(v(i)*(1 - v(i))))/2;
            J(i+N+2,i+N+3) = -cv/h(i);
            J(i+N+2,i+N+1) = -cv/h(i-1);
            
            J(i+N+2,i) = (h(i-1) + h(i))*nyv*fyv/2;
            J(i+N+2,i+2*N+4) = (h(i-1) + h(i))*nv*F;
            J(i+N+2,3*N+6) = (h(i-1) + h(i))/2;
        end
        J(2*N+4,2*N+4) = cv/h(N+1) + h(N+1)*(2*nvv*fv + nv*R*T/(v(N+2)*(1 - v(N+2))))/2;
        J(2*N+4,2*N+3) = -cv/h(N+1);
        J(2*N+4,N+2) = h(N+1)*nyv*fyv/2;
        J(2*N+4,3*N+6) = h(N+1)/2;
        
        J(2*N+5,2*N+5) = -epsr*eps0/h(1);
        J(2*N+5,2*N+6) = epsr*eps0/h(1);
        J(2*N+5,N+3) = h(1)*F*nv;
        J(2*N+5,1) = -h(1)*F*ny/2;
        for i=2:N
            J(i+2*N+4,i+2*N+4) = -epsr*eps0*(1/h(i-1) + 1/h(i));
            J(i+2*N+4,i+2*N+3) = epsr*eps0/h(i-1);
            J(i+2*N+4,i+2*N+5) = epsr*eps0/h(i);
            
            J(i+2*N+4,i+N+2) = (h(i-1) + h(i))*F*nv;
            J(i+2*N+4,i) = -(h(i-1) + h(i))*F*ny/2;
        end
        J(3*N+5,3*N+5) = -epsr*eps0*(1/h(N) + 1/h(N+1));
        J(3*N+5,3*N+4) = epsr*eps0/h(N);
        J(3*N+5,2*N+3) = (h(N) + h(N+1))*nv*F;
        J(3*N+5,N+1) = -(h(N) + h(N+1))*ny*F/2;
        
        J(3*N+6,1) = h(1)/2;
        for i=2:N+1
            J(3*N+6,i) = (h(i-1) + h(i))/2;
        end
        J(3*N+6,N+2) = h(N+1)/2;
        
        J(3*N+7,N+3) = h(1)/2;
        for i=2:N+1
            J(3*N+7,i+N+2) = (h(i-1) + h(i))/2;
        end
        J(3*N+7,2*N+4) = h(N+1)/2;
        
        s = J\f;
        
        arlam = 1;
        while (1)
            
            xtest = x - arlam*s;
            y(1:N+2) = xtest(1:N+2);
            v(1:N+2) = xtest(N+3:2*N+4);
            phi(1:N+1) = xtest(2*N+5:3*N+5);
            lamv = xtest(3*N+6);
            lambd = xtest(3*N+7);
            
            ftest(1) = cd*(y(1)/h(1) - y(2)/h(1)) + h(1)*(2*nyy*fy*y(1) + nyv*fyv*v(1) + ny*R*T*log(y(1)/(1-y(1))) - ny*F*phi(1) + lambd)/2;
            for i=2:N+1
                ftest(i) = cd*(-y(i-1)/h(i-1) + y(i)*(1/h(i-1) + 1/h(i)) - y(i+1)/h(i)) + (h(i-1) + h(i))*(2*nyy*fy*y(i) + nyv*fyv*v(i) + ny*R*T*log(y(i)/(1-y(i))) - ny*F*phi(i) + lambd)/2;
            end
            ftest(N+2) = cd*(-y(N+1)/h(N+1) + y(N+2)/h(N+1)) + h(N+1)*(2*nyy*fy*y(N+2) + nyv*fyv*v(N+2) + ny*R*T*log(y(N+2)/(1-y(N+2))) + lambd)/2;
            
            ftest(N+3) = cv*(v(1)/h(1) - v(2)/h(1)) + no*fo + h(1)*(2*nvv*fv*v(1) + nyv*fyv*y(1) + nv*R*T*log(v(1)/(1-v(1))) + nv*2*F*phi(1) + lamv)/2;
            for i=2:N+1
                ftest(N+2+i) = cv*(-v(i-1)/h(i-1) + v(i)*(1/h(i-1) + 1/h(i)) - v(i+1)/h(i)) + (h(i-1) + h(i))*(2*nvv*fv*v(i) + nyv*fyv*y(i) + nv*R*T*log(v(i)/(1-v(i))) + nv*2*F*phi(i) + lamv)/2;
            end
            ftest(2*N+4) = cv*(-v(N+1)/h(N+1) + v(N+2)/h(N+1)) + h(N+1)*(2*nvv*fv*v(N+2) + nyv*fyv*y(N+2) + nv*R*T*log(v(N+2)/(1-v(N+2))) + lamv)/2;
            
            ftest(2*N+5) = epsr*eps0*(-phi(1)/h(1) + phi(2)/h(1)) + h(1)*F*(2*nv*v(1) - ny*y(1))/2;
            for i=2:N
                ftest(2*N+4+i) = epsr*eps0*(phi(i-1)/h(i-1) - phi(i)*(1/h(i-1) + 1/h(i)) + phi(i+1)/h(i)) + (h(i-1) + h(i))*F*(2*nv*v(i) - ny*y(i))/2;
            end
            ftest(3*N+5) = epsr*eps0*(phi(N)/h(N) - phi(N+1)*(1/h(N) + 1/h(N+1))) + (h(N) + h(N+1))*F*(2*nv*v(N+1) - ny*y(N+1))/2;
            
            ftest(3*N+6) = (y(1) - yd)*h(1)/2;
            for i=2:N+1
                ftest(3*N+6) = ftest(3*N+6) + (y(i) - yd)*(h(i-1) + h(i))/2;
            end
            ftest(3*N+6) = ftest(3*N+6) + (y(N+2) - yd)*h(N+1)/2;
            
            ftest(3*N+7) = (v(1) - vd)*h(1)/2;
            for i=2:N+1
                ftest(3*N+7) = ftest(3*N+7) + (v(i) - vd)*(h(i-1) + h(i))/2;
            end
            ftest(3*N+7) = ftest(3*N+7) + (v(N+2) - vd)*h(N+1)/2;
            
            if (norm(imag(ftest)) == 0 && norm(ftest) < norm(f)*(1 + 1e-4/arlam))
                x = xtest;
                f = ftest;
                break;
            else
                arlam = arlam/2;
            end
            
        end
        
        nf = norm(f)/length(f);
        its = its + 1;
        
    end
    
    % solver failure at 1000 Newton iterations without convergence
    if (its == 1000)
        flag = 0;
        break;
    end
    
    if (refnum > 1)
    
        for i=1:length(nodes)
            if nodes(i) == vnod;
                ivnod = i;
            end
            if nodes(i) == ynod;
                iynod = i;
            end
            if nodes(i) == phinod;
                iphinod = i;
            end
        end

        if ((abs(v(ivnod) - vmax)/vmax < 1e-3 && abs(y(iynod) - ymax)/ymax < 1e-3 && abs(phi(iphinod) - phimax)/phimax < 1e-3))
            flag = 1;
            break;
        end
    end
    
    if (min(h) < 1e-11)
        flag = 1;
        break;
    end
    
    ffy = zeros(N+2,1);
    ffv = zeros(N+2,1);
    ffphi = zeros(N+2,1);
    
    erry = zeros(size(h));
    errv = zeros(size(h));
    errphi = zeros(size(h));
    
    % local error calculation: nodes
    for i=1:length(h)
        ffy(i) = 2*nyy*fy*y(i) + nyv*fyv*v(i) + ny*R*T*log(y(i)/(1-y(i))) - ny*F*phi(i) + lambd;
        ffv(i) = 2*nvv*fv*v(i) + nyv*fyv*y(i) + nv*R*T*log(v(i)/(1-v(i))) + nv*2*F*phi(i) + lamv;
        ffphi(i) = F*(2*nv*v(i) - ny*y(i));
    end
    ffy(N+2) = 2*nyy*fy*y(N+2) + nyv*fyv*v(N+2) + ny*R*T*log(y(N+2)/(1-y(N+2))) + lambd;
    ffv(N+2) = 2*nvv*fv*v(N+2) + nyv*fyv*y(N+2) + nv*R*T*log(v(N+2)/(1-v(N+2))) + lamv;
    ffphi(N+2) = F*(2*nv*v(N+2) - ny*y(N+2));
    
    % local error calculation: elements
    for i=1:length(h)
        erry(i) = h(i)^3*(ffy(i)^2 + ffy(i+1)^2)/2;
        errv(i) = h(i)^3*(ffv(i)^2 + ffv(i+1)^2)/2;
        errphi(i) = h(i)^3*(ffphi(i)^2 + ffphi(i+1)^2)/2;
    end
    
    [~,vind] = max(errv);
    [~,yind] = max(erry);
    [~,phind] = max(errphi);
    vnod = nodes(vind);
    ynod = nodes(yind);
    phinod = nodes(phind);
    vmax = v(vind);
    ymax = y(yind);
    phimax = phi(phind);
    
    %remeshing & interpolation
    if refnum == 1
        minerry = min(erry);
        minerrv = min(errv);
        minerrphi = min(errphi);
        
        maxerry = max(erry);
        maxerrv = max(errv);
        maxerrphi = max(errphi);
        
        threshy = 1e-2*(maxerry - minerry) + minerry;
        threshv = 1e-2*(maxerrv - minerrv) + minerrv;
        threshphi = 1e-2*(maxerrphi - minerrphi) + minerrphi;
    end
    
    refmesh = zeros(size(h));
    for i=1:size(h)
        
        if (erry(i) > threshy || errv(i) > threshv || errphi(i) > threshphi)
            refmesh(i) = 1;
        end
        
    end
    
    % routine ends with success when all elements meet the standard for
    % error
    if sum(refmesh) == 0
        phi = [phi; 0];
        flag = 1;
        break;
    end
    
    newnodes = zeros(length(nodes) + sum(refmesh),1);
    newy = newnodes;
    newv = newnodes;
    newphi = newnodes;
    
    
    phi = [phi; 0];
    nodind = 1;
    for i=1:length(refmesh)
        
        newnodes(nodind) = nodes(i);
        newy(nodind) = y(i);
        newv(nodind) = v(i);
        newphi(nodind) = phi(i);
        
        if (refmesh(i))
            newnodes(nodind+1) = (nodes(i) + nodes(i+1))/2;
            newy(nodind+1) = (y(i) + y(i+1))/2;
            newv(nodind+1) = (v(i) + v(i+1))/2;
            newphi(nodind+1) = (phi(i) + phi(i+1))/2;
            nodind = nodind + 2;
        else
            nodind = nodind + 1;
        end
    end
    
    newN = length(newnodes) - 2;
    
    newnodes(newN+2) = nodes(N+2);
    newy(newN+2) = y(N+2);
    newv(newN+2) = v(N+2);
    newphi(newN+2) = [];
    
    N = newN;
    
    h = zeros(N+1,1);
    
    for i=1:length(h)
        h(i) = newnodes(i+1) - newnodes(i);
    end
    
    nodes = newnodes;
    v = newv;
    y = newy;
    phi = newphi;
    
    refnum = refnum + 1;
    
end

warning('on', 'MATLAB:nearlySingularMatrix');

end