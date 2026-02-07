%% Example 7.3  Robbins–Monro 随机逼近求均值
%% 参
L = 500;               
mu = 2;                 
sigma = 1;              

%% 观测
z = mu + sigma * randn(L,1);

%% R-M 算法
x_hat = zeros(L,1);
x_hat(1) = z(1);

for k = 2:L
    rho = 1/k;
    x_hat(k) = x_hat(k-1) + rho * (z(k) - x_hat(k-1));
end

%% 解
x_mean = cumsum(z) ./ (1:L)';

%% 绘图
figure;
plot(x_hat,'LineWidth',1.5); hold on;
plot(x_mean,'--','LineWidth',1.5);
yline(mu,'k:','LineWidth',1.5);
legend('R-M 估计','样本均值','真实均值');
xlabel('k'); ylabel('x');
title('Example 7.3 随机逼近求均值');
grid on;
