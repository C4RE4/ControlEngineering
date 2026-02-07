%% 参数
L = 2000;
theta0 = [-0.18; 0.784; -0.656];
na = 3;

sigma_v2 = 1;
sigma_w2 = 0.25;

%% 噪声
v = sqrt(sigma_v2)*randn(L,1);
w = sqrt(sigma_w2)*randn(L,1);

%% 系统输出
y = zeros(L,1);
for k = 4:L
    y(k) = -theta0(1)*y(k-1) ...
           -theta0(2)*y(k-2) ...
           -theta0(3)*y(k-3) ...
           + v(k);
end
z = y + w;

%% 初始化
theta_hat1 = zeros(na,L);   % 算法 (7.6.35)
theta_hat2 = zeros(na,L);   % 算法 (7.6.38)

%% 随机逼近
for k = 4:L-1
    h = [-z(k); -z(k-1); -z(k-2)];
    e1 = z(k+1) - h.'*theta_hat1(:,k);
    e2 = z(k+1) - h.'*theta_hat2(:,k);

    rho = 1/k;

    % (7.6.35) 基本随机逼近
    theta_hat1(:,k+1) = theta_hat1(:,k) + rho * h * e1;

    % (7.6.38) 修正随机逼近 RSAA
    theta_hat2(:,k+1) = theta_hat2(:,k) ...
        + rho * ( h * e2 + sigma_w2 * eye(na) * theta_hat2(:,k) );
end

%% 误差范数
err1 = vecnorm(theta_hat1 - theta0,2,1).^2 / norm(theta0)^2;
err2 = vecnorm(theta_hat2 - theta0,2,1).^2 / norm(theta0)^2;

%% 绘图
figure;
semilogy(err1,'LineWidth',1.5); hold on;
semilogy(err2,'LineWidth',1.5);
legend('(7.6.35) 随机逼近','(7.6.38) 修正算法');
xlabel('k'); ylabel('归一化参数误差');
title('Example 7.4 随机逼近算法性能比较');
grid on;
