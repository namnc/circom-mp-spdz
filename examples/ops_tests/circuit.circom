pragma circom 2.1.0;



template mpspdz(N) {

    // ADD = 'AAdd'

    signal input in1_add[N];
    signal input in2_add[N];
    signal output out_add[N];

    for (var i = 0; i < N; i++) {
        out_add[i] <== in1_add[i] + in2_add[i];
    }
    

    // DIV = 'ADiv'
    
    signal input in1_div[N];
    signal input in2_div[N];
    signal output out_div[N];

    for (var i = 0; i < N; i++) {
        out_div[i] <== in1_div[i] / in2_div[i];
    }

    // EQ = 'AEq'

    signal input in1_eq[N];
    signal input in2_eq[N];
    signal output out_eq[N];

    for (var i = 0; i < N; i++) {
       out_eq[i] <== in1_eq[i] == in2_eq[i];
    }
    
    // GT = 'AGt'

    signal input in1_gt[N];
    signal input in2_gt[N];
    signal output out_gt[N];

    for (var i = 0; i < N; i++) {
       out_gt[i] <== in1_gt[i] > in2_gt[i];
    }

    // GEQ = 'AGEq'

    signal input in1_geq[N];
    signal input in2_geq[N];
    signal output out_geq[N];

    for (var i = 0; i < N; i++) {
       out_geq[i] <== in1_geq[i] >= in2_geq[i];
    }

    // LT = 'ALt'

    signal input in1_lt[N];
    signal input in2_lt[N];
    signal output out_lt[N];

    for (var i = 0; i < N; i++) {
       out_lt[i] <== in1_lt[i] < in2_lt[i];
    }
    
    // LEQ = 'ALEq'

    signal input in1_leq[N];
    signal input in2_leq[N];
    signal output out_leq[N];

    for (var i = 0; i < N; i++) {
       out_leq[i] <== in1_leq[i] <= in2_leq[i];
    }
    
    // MUL = 'AMul'

    signal input in1_mul[N];
    signal input in2_mul[N];
    signal output out_mul[N];

    for (var i = 0; i < N; i++) {
       out_mul[i] <== in1_mul[i] * in2_mul[i];
    }

    // NEQ = 'ANeq'

    signal input in1_neq[N];
    signal input in2_neq[N];
    signal output out_neq[N];

    for (var i = 0; i < N; i++) {
       out_neq[i] <== in1_neq[i] != in2_neq[i];
    }
    
    // SUB = 'ASub'

    signal input in1_sub[N];
    signal input in2_sub[N];
    signal output out_sub[N];

    for (var i = 0; i < N; i++) {
       out_sub[i] <== in1_sub[i] - in2_sub[i];
    }

    // Below can only do with latest compiler

    // XOR = 'AXor',

   //  signal input in1_xor[N];
   //  signal input in2_xor[N];
   //  signal output out_xor[N];

   //  for (var i = 0; i < N; i++) {
   //     out_xor[i] <== in1_xor[i] ^ in2_xor[i];
   //  }

    // POW = 'APow',

    signal input in1_pow[N];
    signal input in2_pow[N];
    signal output out_pow[N];

    for (var i = 0; i < N; i++) {
       out_pow[i] <== in1_pow[i] ** in2_pow[i];
    }
    
    // IDIV = 'AIntDiv',

    signal input in1_idiv[N];
    signal input in2_idiv[N];
    signal output out_idiv[N];

    for (var i = 0; i < N; i++) {
       out_idiv[i] <== in1_idiv[i] \ in2_idiv[i];
    }

    // MOD = 'AMod',

   //  signal input in1_mod[N];
   //  signal input in2_mod[N];
   //  signal output out_mod[N];

   //  for (var i = 0; i < N; i++) {
   //      out_mod[i] <== in1_mod[i] % in2_mod[i];
   //  }

    // SHL = 'AShiftL',

    signal input in1_shl[N];
    signal input in2_shl[N];
    signal output out_shl[N];

    for (var i = 0; i < N; i++) {
        out_shl[i] <== in1_shl[i] << in2_shl[i];
    }

    // SHR = 'AShiftR'

    signal input in1_shr[N];
    signal input in2_shr[N];
    signal output out_shr[N];

    for (var i = 0; i < N; i++) {
        out_shr[i] <== in1_shr[i] >> in2_shr[i];
    }   
}

component main = mpspdz(100);
