FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    automake build-essential clang cmake git \
    libboost-dev libclang-dev libboost-iostreams-dev libboost-thread-dev \
    libboost-filesystem-dev libgmp-dev libntl-dev libsodium-dev libssl-dev libtool \
    python3 python3-pip curl

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /testing

RUN git clone https://github.com/namnc/circom-mp-spdz.git && \
    git clone https://github.com/namnc/circom-2-arithc.git && \
    git clone https://github.com/mhchia/MP-SPDZ.git

RUN cd circom-2-arithc && cargo build --release
RUN cd MP-SPDZ && git checkout 704049e && make -j8 semi-party.x

EXPOSE 5000

CMD ["/bin/bash"]