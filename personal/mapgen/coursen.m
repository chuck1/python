function [ Z2 ] = coursen( Z,F )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
sz = (size(Z)-1)/F+1;
Z2 = zeros(sz);
for a = 1:size(Z2,1)
    for b = 1:size(Z2,2)
        Z2(a,b) = Z(2*a-1,2*b-1);
    end
end

end

