function [ h ] = FIR2( N,sigma )
%UNTITLED8 Summary of this function goes here
%   Detailed explanation goes here

% [f1,f2] = freqspace(N,'meshgrid');
% Hd = ones(N);
% r = sqrt(f1.^2 + f2.^2);

% Hd(r>f) = 0;
% 
% win = fspecial('gaussian',N,sigma);
% win = win ./ max(win(:));  % Make the maximum window value be 1.
% 
% h = fwind2(Hd,win);

h = fspecial('gaussian',N,sigma);

end

