%% Example 7.5  随机梯度校正法在线辨识（Mendel, 1972）
clear; clc;

%% 已知参数与仿真设置
Ts = 0.01;                 
Tend = 0.5;
N = round(Tend/Ts);       
k1 = 52;                   

sigma_theta = 0.061;       
sigma_alpha = 0.016;       
sigma_delta = 3.0;         

Lambda1 = 0.1;
Lambda2 = 1;

Ma_true = 500;
Ms_true = 1000;
Za_true = 1;               

%% 输入 Ni(k)
Ni = zeros(N,1);
Ni(1:round(0.1/Ts))  = 10;
Ni(round(0.1/Ts)+1:round(0.2/Ts)) = 20;
Ni(round(0.2/Ts)+1:round(0.3/Ts)) = 30;
Ni(round(0.3/Ts)+1:round(0.4/Ts)) = 40;
Ni(round(0.4/Ts)+1:end) = 50;

%% 状态与测量量
alpha = zeros(N,1);
delta = zeros(N,1);
thetadd = zeros(N,1);
Na = zeros(N,1);

% 测量噪声
wa = sqrt(sigma_alpha)*randn(N,1);
wd = sqrt(sigma_delta)*randn(N,1);
wt = sqrt(sigma_theta)*randn(N,1);
wN = sqrt(0.01)*randn(N,1);

%% 参数估计初值
Ma_hat = zeros(N,1);  Ma_hat(1) = 250;
Ms_hat = zeros(N,1);  Ms_hat(1) = 500;
Za_hat = zeros(N,1);  Za_hat(1) = 0.5;

%% 仿真与辨识
for k = 1:N-1
    % 动力学关系
    alpha(k)   = 0.01*Ni(k);
    delta(k)   = 0.5*alpha(k);
    thetadd(k) = Ma_true*alpha(k) + Ms_true*delta(k);
    Na(k)      = Za_true*alpha(k);

    % 测量值
    am = alpha(k)   + wa(k);
    dm = delta(k)   + wd(k);
    tm = thetadd(k) + wt(k);
    Nam = Na(k)     + wN(k);

    % 估计误差
    t_tilde = tm - Ma_hat(k)*am - Ms_hat(k)*dm;
    N_tilde = Nam - Za_hat(k)*am;

    if k <= k1
       
        Ma_hat(k+1) = (1 + Lambda1*sigma_alpha/(Lambda1*am^2+Lambda2*dm^2))*Ma_hat(k) ...
                       + Lambda1*am*t_tilde/(Lambda1*am^2+Lambda2*dm^2);

        Ms_hat(k+1) = (1 + Lambda2*sigma_delta/(Lambda1*am^2+Lambda2*dm^2))*Ms_hat(k) ...
                       + Lambda2*dm*t_tilde/(Lambda1*am^2+Lambda2*dm^2);

        Za_hat(k+1) = (1 + sigma_theta/am^2)*Za_hat(k) + N_tilde/am;
    else
      
        Ma_hat(k+1) = (1 + Lambda1*sigma_alpha/k)*Ma_hat(k) + Lambda1*am*t_tilde/k;
        Ms_hat(k+1) = (1 + Lambda2*sigma_delta/k)*Ms_hat(k) + Lambda2*dm*t_tilde/k;
        Za_hat(k+1) = (1 + sigma_theta/k)*Za_hat(k) + am*N_tilde/k;
    end
end

%% 结果绘图
t = (0:N-1)*Ts;
figure;
subplot(3,1,1); plot(t,Ma_hat,'LineWidth',1.2); grid on;
ylabel('\hat M_a'); 

subplot(3,1,2); plot(t,Ms_hat,'LineWidth',1.2); grid on;
ylabel('\hat M_s');

subplot(3,1,3); plot(t,Za_hat,'LineWidth',1.2); grid on;
ylabel('\hat Z_a'); xlabel('Time (s)');
