#!/bin/bash
# Download script for Pruning_Efficiency reconstruction papers

mkdir -p papers

download_paper() {
    local name="$1"
    local url="$2"
    local filename="$3"
    local output_path="papers/$filename"
    
    if [ -f "$output_path" ]; then
        echo "Already downloaded: $name"
    else
        echo "Downloading $name..."
        wget -q -O "$output_path" "$url"
        echo "Finished downloading: $name"
    fi
}

download_paper "Saliency-Guided Primitive Merging" "https://arxiv.org/pdf/2608.10712v1.pdf" "ArXiv2026_SaliencyGuidedMerging.pdf" &
download_paper "G2ARD-GS" "https://arxiv.org/pdf/2608.05704v1.pdf" "ArXiv2026_G2ARDGS.pdf" &
download_paper "DecoupleGS" "https://arxiv.org/pdf/2608.01761v1.pdf" "ECCV2026_DecoupleGS.pdf" &
download_paper "D2-4DGS" "https://arxiv.org/pdf/2608.01588v1.pdf" "ArXiv2026_D24DGS.pdf" &
download_paper "AtlasLC" "https://arxiv.org/pdf/2607.26525v1.pdf" "ISMAR2026_AtlasLC.pdf" &
download_paper "CaT-GS" "https://arxiv.org/pdf/2607.17842v1.pdf" "CVPR2026_CaTGS.pdf" &
download_paper "Flux-GS" "https://arxiv.org/pdf/2606.30017v1.pdf" "ECCV2026_FluxGS.pdf" &
download_paper "MVFusion-GS" "https://arxiv.org/pdf/2607.01578v2.pdf" "ArXiv2026_MVFusionGS.pdf" &
download_paper "Flow Splatting" "https://arxiv.org/pdf/2606.29976v1.pdf" "ArXiv2026_FlowSplatting.pdf" &

download_paper "Z-Order Transformer" "https://arxiv.org/pdf/2605.13465v1.pdf" "CVPR2026_ZOrderTransformer.pdf" &
download_paper "Gaussian-Voxel Duet" "https://arxiv.org/pdf/2605.26616v1.pdf" "ArXiv2026_GaussianVoxelDuet.pdf" &
download_paper "PLANING" "https://arxiv.org/pdf/2601.22046v4.pdf" "ArXiv2026_PLANING.pdf" &
download_paper "DLGStream" "https://arxiv.org/pdf/2606.28840v1.pdf" "ECCV2026_DLGStream.pdf" &
download_paper "Eulerian Gaussian Splatting" "https://arxiv.org/pdf/2605.29136v1.pdf" "CVPR2026_EulerianGaussianSplatting.pdf" &
download_paper "CAdam" "https://arxiv.org/pdf/2605.20872v1.pdf" "SIGGRAPH2026_CAdam.pdf" &

echo "Waiting for all downloads to finish..."
wait
echo "All downloads completed."
