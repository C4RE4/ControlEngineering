%% 参数
L = 200;                 
na_set = 1:4;            
nb_set = 1:4;            
nd_set = 1:4;           

%% 输入与噪声 
u = idinput(L,'prbs',[-1 1]);

e = randn(L,1);
v = zeros(L,1);
for k = 2:L
    v(k) = 0.9*v(k-1) + e(k);
end

%% 系统 
z = zeros(L,1);
for k = 3:L
    z(k) = 1.5*z(k-1) - 0.7*z(k-2) ...
         + 1.2*u(k-1) - 0.5*u(k-2) ...
         + v(k);
end

%% MFPE
MFPE = inf(length(na_set),length(nb_set),length(nd_set));

for ia = 1:length(na_set)
    for ib = 1:length(nb_set)
        for id = 1:length(nd_set)

            na = na_set(ia);
            nb = nb_set(ib);
            nd = nd_set(id);

            maxlag = max([na nb nd]);
            Phi = [];
            y = z(maxlag+1:end);

            for k = maxlag+1:L
                phi_k = [];

                % 输出项
                for i = 1:na
                    phi_k = [phi_k, -z(k-i)];
                end

                % 输入项
                for i = 1:nb
                    phi_k = [phi_k, u(k-i)];
                end

                % 噪声模型
                for i = 1:nd
                    phi_k = [phi_k, -v(k-i)];
                end

                Phi = [Phi; phi_k];
            end

            % 最小二乘
            theta_hat = (Phi' * Phi) \ (Phi' * y);
            y_hat = Phi * theta_hat;
            res = y - y_hat;

            % 残差方差
            sigma2_v = (res' * res) / length(res);

            % 二阶导数近似为 Fisher 信息矩阵
            H = (Phi' * Phi) / length(res);
            trace_term = trace(inv(H));

            MFPE(ia,ib,id) = sigma2_v * (1 + trace_term);
        end
    end
end

%% 最优阶次
[minMFPE, idx] = min(MFPE(:));
[ia_opt, ib_opt, id_opt] = ind2sub(size(MFPE), idx);

%% 输出
fprintf('最优组合：na = %d, nb = %d, nd = %d\n', ...
        na_set(ia_opt), nb_set(ib_opt), nd_set(id_opt));
fprintf('最小 MFPE 值：%.4f\n', minMFPE);

