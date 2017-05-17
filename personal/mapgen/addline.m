function [ Z2 ] = addline( X,Y,Z,x,y,z )
%UNTITLED7 Summary of this function goes here
%   Detailed explanation goes here
dx = X(2,1)-X(1,1);
dy = Y(1,2)-Y(1,1);

Z2 = Z;

m = (y(2)-y(1))/(x(2)-x(1));
b = y(1)-m*x(1);

X2 = (Y-b)/m;
Y2 = m*X+b;

ind = (abs(Y-Y2)<dy)&(abs(X-X2)<dx)&(X<x(2))&(X>x(1))&(Y<y(2))&(Y>y(1));

Z2(ind) = z;

end

