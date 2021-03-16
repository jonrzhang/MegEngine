// generated by gen_cuda_conv_bias_kern_impls.py
#include "../conv_bias_int8_implicit_gemm_imma16x16x16_cdiv4hwn4_reorder_filter.cuinl"

template void megdnn::cuda::conv_bias_int8::do_conv_bias_int8_implicit_gemm_imma16x16x16_cdiv4hwn4_reorder_filter<PerChannelBiasVisitor, 
        IConvEpilogue<Activation<megdnn::param_enumv::ConvBias::NonlineMode::RELU>>>(
        const int8_t* d_src, 
        const int8_t* d_filter, 
        PerChannelBiasVisitor bias, 
        IConvEpilogue<Activation<megdnn::param_enumv::ConvBias::NonlineMode::RELU>> epilogue, 
        const ConvParam& param, 
        float alpha, 
        float beta, 
        cudaStream_t stream);
