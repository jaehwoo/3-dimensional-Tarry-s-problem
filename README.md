# 3-dimensional Tarry's problem

These working manuscripts are shared to invite thorough discussion among professional harmonic analysts. The author does not deserve any credit for uploading them. The purpose of this upload is to encourage careful examination and discussion, rather than to declare a resolution of Tarry's problem.

The manuscripts concern the continous Tarry convergence problem for the full total-degree Parsell-Vinogradov systems in three variables. We show that for the 3-dimensional Tarry's problem for degree $k$, the critical exponent is

```math
p_{3,k}^{\rm Tar}=k+\binom{k+3}{4}.
```

Paper I considers the case $k\ge14$, with shared estimates throughout the whole project. Paper II considers the cases $2\le k\le13$. Supplement paper supplies additional materials used by papers I and II.

The main idea is to make use of complete affine jets. Given an affine transformation $T:u\mapsto c+Bu$ with $c\in\mathbb{R}^3$ and $B\in GL_3(\mathbb{R})$, the coefficient vector of $F(c_Bu)-F(c)$ is called the complete affine jet of $F$ at frame $(c,B)$. Translation in $c$ mixes homogeneous parts of $F$ of different degrees via a unitriangular transformation on $V_k$, the quotient vector space of 3-variable polynomials up to degree $k$, with respect to constants. Acting by $B$ preserves each homogeneous degree, and has determinant $(\det B)^{\frac{1}{3}\binom{j+2}{2}}$ on each degree.

The proof has been checked through ChatGPT Work mode, but is yet to be human-verified. This records AI-assisted verification, with the outstanding work stated below. Lean formalization and verification are still in progress; completed and ongoing work is and will continue to be uploaded to the author's separate public repository, [Tarry-problem-lean-checkpoint-backup](https://github.com/jaehwoo/Tarry-problem-lean-checkpoint-backup). A complete Lean verification of the main theorem is not yet available.

| Manuscript | PDF | LaTeX source | Manuscript status | Lean status |
| --- | --- | --- | --- | --- |
| Paper I (deg >= 14) | [Read](Complete_Affine_Jets_I.pdf) | [Source](Complete_Affine_Jets_I.tex) | Awaits final revision. | In progress; complete verification pending. |
| Paper II (deg <= 13) | [Read](Complete_Affine_Jets_II.pdf) | [Source](Complete_Affine_Jets_II.tex) | Awaits verification, readability enhancement, and final revision. | Complete Lean verification pending. |
| Supplement | [Read](Complete_Affine_Jets_Supplement.pdf) | [Source](Complete_Affine_Jets_Supplement.tex) | Awaits verification, readability enhancement, and final revision. | Complete Lean verification pending. |

The manuscripts are uploaded from their saved working versions. **Paper I version note:** its PDF and LaTeX source both include the four authorized correction groups from the November 2, 2026 revision. The corrected PDF replaces the earlier October 8 snapshot. The Paper I files have been named `Complete_Affine_Jets_I` here to match the companion manuscripts' cross-reference filenames.

## Acknowledgement of the established lower bound

The author has recently become aware that Cheng Bi and Ruichen Sun have established a lower bound for the Tarry convergence exponent in [*L^p integrability of functions with Fourier support on High codimension manifolds*](https://arxiv.org/abs/2610.39739), arXiv:2610.39739. Their established lower bound is acknowledged here. This acknowledgement supplements the literature discussion in the working manuscripts, which still awaits revision.

## Contact

email: wjhwsh1@snu.ac.kr
