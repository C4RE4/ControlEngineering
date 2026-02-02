clc; clear; close all;

%% 参数
T0 = 0.4;          % 采样时间
L  = 1000;         % 数据长度
M  = 150;          % 最大滞后
r  = 0:M;
omega = r*pi/(M*T0);

%% 白噪声
v = randn(L,1);           % v(k) ~ N(0,1)
w = 0.2*randn(L,1);       % w(k) ~ N(0,0.04)

%% 成形滤波器
num1 = sqrt(0.4);
den1 = [1 -0.64];
u = filter(num1, den1, v);

%% 被辨识对象
num2 = [0 0 0.0576];
den2 = [1 -1.76 0.8176];
y = filter(num2, den2, u);

%% 输出加噪声
z = y + w;

%% 样本相关函数估计
% 去均值
u = u - mean(u);
z = z - mean(z);
% 自相关 & 互相关
Ruu = zeros(M+1,1);
Ruz = zeros(M+1,1);

for l = 0:M
    Ruu(l+1) = (1/L)*sum(u(1:L-l).*u(1+l:L));
    Ruz(l+1) = (1/L)*sum(u(1:L-l).*z(1+l:L));
end

%% 样本谱
Suu = zeros(M+1,1);
Luz = zeros(M+1,1);
Quz = zeros(M+1,1);

for r = 0:M
    Suu(r+1) = Ruu(1) + 2*sum(Ruu(2:end).*cos(r*(1:M)'*pi/M));
    Luz(r+1) = Ruz(1) + 2*sum(Ruz(2:end).*cos(r*(1:M)'*pi/M));
    Quz(r+1) = 2*sum(Ruz(2:end).*sin(r*(1:M)'*pi/M));
end

%% Hanning 平滑
a = [0.25 0.5 0.25];

Suu_s = zeros(M+1,1);
Luz_s = zeros(M+1,1);
Quz_s = zeros(M+1,1);

for r = 2:M
    Suu_s(r) = a(1)*Suu(r-1) + a(2)*Suu(r) + a(3)*Suu(r+1);
    Luz_s(r) = a(1)*Luz(r-1) + a(2)*Luz(r) + a(3)*Luz(r+1);
    Quz_s(r) = a(1)*Quz(r-1) + a(2)*Quz(r) + a(3)*Quz(r+1);
end

%% 延迟补偿
[~,l0] = max(abs(Ruz));
l0 = l0 - 1;

Luz_c = zeros(M+1,1);
Quz_c = zeros(M+1,1);

for r = 0:M
    phi = r*l0*pi/M;
    Luz_c(r+1) = Luz_s(r+1)*cos(phi) - Quz_s(r+1)*sin(phi);
    Quz_c(r+1) = Luz_s(r+1)*sin(phi) + Quz_s(r+1)*cos(phi);
end

%% 幅频 & 相频
G_est = sqrt((Luz_c.^2 + Quz_c.^2)./Suu_s);
theta_est = -atan2(Quz_c, Luz_c);

%% 理论频响
z_tf = tf(num2, den2, T0);
[mag, phase] = bode(z_tf, omega);
mag = squeeze(mag);
phase = squeeze(phase);

figure;
subplot(2,1,1)
plot(omega, mag, 'k', omega, G_est, 'r--','LineWidth',1.2)
xlabel('\omega'); ylabel('|G(j\omega)|')
legend('理论','平滑谱估计')
grid on

subplot(2,1,2)
plot(omega, phase, 'k', omega, theta_est, 'r--','LineWidth',1.2)
xlabel('\omega'); ylabel('\angle G(j\omega)')
grid on






