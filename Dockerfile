FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    automake build-essential clang cmake git \
    libboost-dev libclang-dev libboost-iostreams-dev libboost-thread-dev \
    libboost-filesystem-dev libgmp-dev libntl-dev libsodium-dev libssl-dev libtool \
    python3 python3-pip curl \
    iproute2 iperf3 net-tools iputils-ping \
    nano netcat telnet openssh-server

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /testing

RUN git clone https://github.com/namnc/circom-mp-spdz.git && \
    git clone https://github.com/namnc/circom-2-arithc.git && \
    git clone https://github.com/mhchia/MP-SPDZ.git

RUN cd circom-2-arithc && cargo build --release
RUN cd MP-SPDZ && git checkout 704049e && make -j8 semi-party.x && mkdir Player-Data
RUN cd circom-mp-spdz && git checkout ml_tests

# SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 3000
EXPOSE 5201
EXPOSE 22

CMD ["/bin/bash"]