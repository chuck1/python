function [ Z2 ] = cut_off( Z,z,opt )
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here
Z2 = Z;
switch opt
    case 'above'
        Z2(Z>z) = z;
    case 'below'
        Z2(Z<z) = z;
    otherwise
end

end

