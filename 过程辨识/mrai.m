%% 实例参数

A = [1 1.3 -0.22 -0.832 -0.269];
B = 1;

na = 4;
nb = 1;

theta_true = [1.3; -0.22; -0.832; -0.269; 1];

L = 4000;

u = idinput(L,'prbs',[0 1/1023],[-1 1]);

%% 噪声选择

noise_type = 2; 
% 1: n=0
% 2: n=v
% 3: n=1/A v
% 4: n=D/A v

sigma_v = 0.1;
v = sigma_v*randn(L,1);

D = [1 -0.3 0.1 0.4 -0.15];

switch noise_type
    case 1
        n = zeros(L,1);
    case 2
        n = v;
    case 3
        n = filter(1,A,v);
    case 4
        n = filter(D,A,v);
end

%% 真实系统输出


z = filter(B,A,u) + n;

%% RMR-A 参数设置


beta = [0.814 -0.390 -0.547 -0.135]';

P = 10*eye(na+nb);
Q = 0.1*P;

theta_I = zeros(na+nb,1);
theta = zeros(na+nb,1);

zm = zeros(L,1);
eps_hist = zeros(L,1);
delta_theta = zeros(L,1);

%% 主循环


for k = max(na,nb)+1:L
    
    % 构造 hm(k)
    hm = [-zm(k-1);
          -zm(k-2);
          -zm(k-3);
          -zm(k-4);
           u(k-1)];
       
    % 先验误差
    z_pred_I = theta_I' * hm;
    tilde_z = z(k) - theta' * hm;
    
    eps0 = z(k) - z_pred_I;
    
    % 加补偿项
    for i=1:na
        if k-i > 0
            eps0 = eps0 + beta(i)*(z(k-i) - zm(k-i));
        end
    end
    
    denom = 1 + hm'*(P+Q)*hm;
    
    % 更新积分项
    theta_I = theta_I + (P*hm*eps0)/denom;
    
    % 更新比例项
    theta_P = (Q*hm*eps0)/denom;
    
    theta = theta_I + theta_P;
    
    % 更新输出
    zm(k) = theta' * hm;
    
    % 参数误差距离
    delta_theta(k) = norm(theta - theta_true);
end

%% 图


figure;
plot(delta_theta,'LineWidth',1.5);
xlabel('k');
ylabel('\delta_\theta(k)');
title('RMR-A 参数误差收敛曲线');
grid on;

disp('真实参数:');
disp(theta_true');

disp('最终估计值:');
disp(theta');
