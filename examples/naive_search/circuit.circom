pragma circom 2.0.0;



template naive_search() {
   var N = 1000;
   signal input in1[N];
   signal input in2;
   signal output out;
   signal matches[N];
   signal sum[N];

   sum[0] <== 0 + 0;
   matches[0] <== in2 == in1[0];

   for (var i = 1; i < N; i++) {
      matches[i] <== in2 == in1[i];
      sum[i] <== sum[i-1] + matches[i];
   }

   out <== sum[N-1];
}

component main = naive_search();
