%% 参数
L = 1024;
na_set = 1:4;
nb_set = 1:4;

%% 输入和噪声
u = randn(L,1);
v = randn(L,1);

%% 例题给定系统
z = zeros(L,1);
for k = 4:L
    z(k) = 1.8*z(k-1) - 1.3*z(k-2) + 0.4*z(k-3) ...
         + 1.1*u(k-1) + 0.288*u(k-2) + v(k);
end

%% 去初始非平稳段
z = z(301:end);
u = u(301:end);
L = length(z);

%% AIC
AIC = zeros(length(na_set), length(nb_set));

for ia = 1:length(na_set)
    for ib = 1:length(nb_set)
        na = na_set(ia);
        nb = nb_set(ib);

        maxlag = max(na, nb);
        Phi = [];
        y = z(maxlag+1:end);

        for k = maxlag+1:L
            phi_k = [];
            for i = 1:na
                phi_k = [phi_k, -z(k-i)];
            end
            for i = 1:nb
                phi_k = [phi_k, u(k-i)];
            end
            Phi = [Phi; phi_k];
        end

        %% 最小二乘估计
        theta_hat = (Phi' * Phi) \ (Phi' * y);
        y_hat = Phi * theta_hat;
        e = y - y_hat;

        sigma2 = (e' * e) / length(e);

        %% AIC公式
        AIC(ia, ib) = L * log(sigma2) + 2 * (na + nb);
    end
end

%% 输出
disp('AIC 表（行 na，列 nb）：');
disp(AIC);