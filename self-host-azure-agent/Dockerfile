FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# agent version
ARG AGENT_VERSION=4.255.0

# agent directory
WORKDIR /home/_agentuser/vsts-agent-linux

# copy start.sh
COPY start.sh /home/_agentuser/start.sh

# Install dependencies
RUN apt-get update && \
    apt-get install -y sudo curl unzip software-properties-common git \
    libicu70 libkrb5-3 libssl3 jq \
    libasound2 libffi-dev libx264-dev \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libnspr4 libnss3 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils libxss1 libxtst6 \
    libxshmfence1 libxcb-dri3-0 libglib2.0-0 libgtk-3-0 libx11-xcb1 libxrender1 \
    libdbus-1-3 libxext6 fonts-liberation libappindicator3-1 lsb-release && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create user, group and add to sudo group, install agent
RUN groupadd -g 1000 agentgroup && \
    useradd -m -u 1000 -g agentgroup agentuser && \
    usermod -aG sudo agentuser && \
    echo "agentuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chmod +x /home/_agentuser/start.sh && \
    cd /home/_agentuser/vsts-agent-linux && \
    curl -LsS https://download.agent.dev.azure.com/agent/${AGENT_VERSION}/vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz | tar -xz

# Switch to the azure agentuser
USER agentuser

WORKDIR /home/_agentuser/vsts-agent-linux

ENTRYPOINT ["/home/_agentuser/start.sh"]
