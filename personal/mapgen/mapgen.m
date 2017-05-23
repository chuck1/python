close all;clear all;clc
%% master data set

n = 256;
L = 200;
d = L/n;

x = 0:d:L;
y = 0:d:L;

[Y,X] = meshgrid(x,y);

% Z = zeros(n+1,n+1);
Z = rand(n+1,n+1);

%% create filter
h = FIR2( n/2,21 );

%% normalize
Z = normalize_map( Z,0,1 );

%% add line
% Z = addline(X,Y,Z,[20 80],[60 180],3);
% Z = addline(X,Y,Z,[40 140],[20 100],3);

%% filter
Z = filter2(h,Z);

%% normalize
Z = normalize_map( Z,0,1 );

figure()
mesh(X,Y,Z)

%% cutoff
% Z = cut_off(Z,0,'below');

% h=figure();
% [C,h] = contourf(X,Y,Z);
% % clabel(C,h);
% colorbar


Z((Z>0)&(Z<=1)) = 1;
Z(Z>1) = 2;
Z((Z<=0)&(Z>=-1))  = -1;
Z(Z<-1) = -2;

figure()
mesh(X,Y,Z)

h = FIR2( n/4,5 );
Z = filter2(h,Z);

figure()
mesh(X,Y,Z)

%% add line
% Z = addline(X,Y,Z,[20 80],[60 180],3);
% Z = addline(X,Y,Z,[40 140],[20 100],3);

[GX,GY] = gradient(Z);
G = sqrt(GX.^2+GY.^2);

G = G/0.16*3;

figure()
mesh(X,Y,G)

Z = Z + G;

figure()
mesh(X,Y,Z)

Z2 = rand(n+1,n+1);

%% create filter
h = FIR2( n/8,4 );

%% normalize
Z2 = normalize_map( Z2,0,1 );

%% filter
Z2 = filter2(h,Z2);

%% normalize
Z2 = normalize_map( Z2,0,0.01 );

figure()
mesh(X,Y,Z2)

figure()
mesh(X,Y,G+Z2)
