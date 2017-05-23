function [ Z2 ] = normalize_map( Z,m,v )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
old_v = var(Z(:));
old_m = mean(Z(:));

Z2 = (Z-old_m)/sqrt(old_v);

Z2 = (Z2+m)*sqrt(v);

end