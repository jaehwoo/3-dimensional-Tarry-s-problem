# Research index: Tarry's problem and the Parsell–Vinogradov system

A source guide to the working manuscripts on continuous Tarry's problem in three variables: the Tarry convergence exponent, polynomial oscillatory integrals, complete affine jets, coefficient-volume determinants, and L^p integrability. Search variants: Parsell-Vinogradov system; three-dimensional Tarry problem; full total-degree polynomial phase.

**Status:** these are manuscript claims offered for discussion. This index checks selected statements and source locations; it does not independently verify their proofs or establish a complete resolution. Paper I awaits final revision; Paper II and the supplement await verification, readability enhancement, and final revision. Human verification and complete Lean verification remain pending.

Locations checked on **7 November 2026**, against manuscript commit [3e95a6b](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/tree/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b) and Lean archive commit [6714b11](https://github.com/jaehwoo/Tarry-problem-lean-checkpoint-backup/tree/6714b11056f950c6f662df0f296a8e1076c6eba2). Source links below are pinned to these versions.

## 1. What is the claimed Tarry convergence exponent in three variables?

For an integer $k\ge2$, use the manuscript's coefficient space and zero-constant representative:

$$
V_k=\mathbb R[x,y,z]_{\le k}/\mathbb R,\qquad N_k=\binom{k+3}{3}-1,\qquad \chi_k=\binom{k+3}{4},
$$

$$
F(x,y,z)=\sum_{1\le|\alpha|\le k}c_\alpha(x,y,z)^\alpha,\qquad
\mathcal I_k(F)=\int_{[0,1]^3}e^{iF(x,y,z)}\,dx\,dy\,dz.
$$

Lebesgue measure is taken over **all nonconstant monomial coefficients** $c_\alpha$; the constant coefficient is quotiented out. This is the continuous integrability problem, rather than an integer-solution counting estimate. [Definitions: Paper I, lines 74–89](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L74-L89).

For every finite $p>0$, both main theorems claim

$$
\mathcal I_k\in L^p(V_k)\quad\Longleftrightarrow\quad p>\chi_k+3.
$$

| Degree range | Manuscript label and source | Verification status |
| --- | --- | --- |
| $k\ge14$ | Paper I, Theorem `root:main`, parts (i)–(ii), [lines 91–97](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L91-L97) | Working-manuscript claim; final revision and complete verification pending. |
| $2\le k\le13$ | Paper II, Theorem `root:main`, parts (i)–(ii), [lines 86–92](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_II.tex#L86-L92) | Working-manuscript claim; verification, readability enhancement, and final revision pending. |

The equivalence includes the proposed divergence at $p=\chi_k+3$. Part (ii) of each theorem separately claims that $F\mapsto\int_{\mathbb R^3}a(x)e^{iF(x)}\,dx$ belongs to $L^p(V_k)$ for $p>\chi_k+3$, for each fixed $a\in C_c^\infty(\mathbb R^3)$, with constants depending on the degree, support, and finitely many smooth seminorms. Part (ii) does not assert an equivalence for every amplitude. No complete Lean correspondence for either main theorem is certified by this index.

## 2. How do complete affine jets control coefficient volume?

**Degree range:** fixed $k\ge2$; the determinant identity is stated in dimension $d\ge1$, and the volume estimate in dimension three.

For a fixed affine frame $T(u)=c+Bu$, $c\in\mathbb R^d$, $B\in\mathrm{GL}_d(\mathbb R)$, set $V_{d,k}=\mathbb R[x_1,\ldots,x_d]_{\le k}/\mathbb R$ and $\mathcal L_TF=[F\circ T]$. In dimension three the complete affine jet is represented by $F(c+Bu)-F(c)$; see Definition `def:complete-jet`, [lines 153–170](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L153-L170).

Paper I, Lemma `an:character` (i), [lines 178–183](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L178-L183), states

$$
|\det\mathcal L_T|=|\det B|^{\binom{k+d}{d+1}}.
$$

Thus in dimension three the exponent is $\chi_k=\binom{k+3}{4}$. Part (ii), [lines 185–189](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L185-L189), gives, for $v=|\det B|$, $K\ge1$ and fixed $M$,

$$
\operatorname{vol}\left\{F:\ |B^T\nabla F(c)|\le K,\quad
\sum_{r=2}^k\|D^rF(c)[B,\ldots,B]\|_{\mathrm{HS}}\le M\right\}
\lesssim_{k,M}K^3v^{-\chi_k}.
$$

**Status:** statement and fixed-frame conventions checked in the manuscript; no new Lean compilation or axiom audit, and no complete Lean correspondence asserted here.

## 3. What is available for regular d-chart sections and controlled factorization?

**Degree range:** $k\ge2$. Paper I, Lemma `reg:d-sections` (i), [lines 3225–3228](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L3225-L3228).

Assume a regular $d$ chart of Lemma `reg:regular-preparation`, with its augmented admissibility, bounded coefficient/physical windows and semialgebraic format, $P\ge2$, and $\sigma_{\min}(L_d)\ge P^{-C}$; $L_d$ omits the $D$ column of the augmented orbit matrix. See [setup, lines 1333–1344](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L1333-L1344) and [preparation, lines 1375–1396](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L1375-L1396). Here $d$ is a [group coordinate](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_I.tex#L435-L440).

The manuscript claims a bounded number of semialgebraic sections $s_\nu(t)$ of uniformly bounded description complexity, with $d(s_\nu(t))=t$, and a bounded list of exceptional fibers. Every assigned state factors as

$$
g=s_\nu(t)u,\qquad u\in\mathcal U_d=\{g:d(g)=0\},\qquad
\|u\|+\|u^{-1}\|\le P^C
$$

in homogeneous affine matrices.

**Related archived conditional Lean declaration:** [`PaperI.ActualSectionFactor.actual_component_section_factor`](https://github.com/jaehwoo/Tarry-problem-lean-checkpoint-backup/blob/6714b11056f950c6f662df0f296a8e1076c6eba2/formalization/current/PaperILean/ActualSectionFactor.lean#L21-L49).

Its explicit inputs include published semialgebraic cell decomposition, path connectedness, compatible Hardt triviality, real semialgebraicity, one-variable Nash regularity, and piecewise Nash extensions. It also assumes a set $E$ specified by boundedly many polynomial sign conditions of bounded degree, the augmented-state window and singular-value bounds, an existing `ComponentSectionAtlas`, and membership in the chosen component-section region.

Under these inputs it constructs the actual relative factor $u=v^{-1}g$, where $v$ is the selected section value in the same $d$ fiber, proves $g=vu$ and $d(u)=0$, and bounds the homogeneous matrix and its actual inverse by an explicit power of $P$.

**Status:** conditional declaration inspected in archived source; not freshly compiled here. This correspondence covers the factorization step, not construction of the atlas, every assertion in part (i), or the unit-interval label count in part (ii). It is not verification of the entire lemma.

## 4. Where are the supplementary arguments and finite certificates?

The [supplement source](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_Supplement.tex) contains supporting arguments and finite certificate descriptions. Selected entry points:

| Degree / setting | Statement or data and source label | Verification status |
| --- | --- | --- |
| $k=3$, two variables | For $0<\beta<10^{-3}$, $K=R^\beta$, and sufficiently large $R$, an affine frequency decomposition with coefficient-independent frames and per-type overlap $\lesssim_\beta K^{A_{\rm ov}}$: Theorem `pl:packet-resolution` (alias `pl:decomposition`), [lines 118–147](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_Supplement.tex#L118-L147). | Supporting manuscript claim; no new proof audit. |
| $k=4$, three variables | Specified model rows give nonzero $34\times34$ sampling minors with tabulated determinant values and output exponent sums: Lemma `low:4:rr:minor_lemma`, [lines 820–853](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_Supplement.tex#L820-L853). | Finite identities stated in the supplement; not recomputed here. |
| $k=7,8$, three variables | Full-column regular sampling certificates and scale minima: section `supp:seven-eight:verification`, [lines 1367–1387](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_Supplement.tex#L1367-L1387). | Certificate description; no fresh execution. |
| $9\le k\le13$, three variables | Fixed sampling rows for 22 cases per degree; degree nine uses the lifted row sets: section `low:row-masks`, [lines 1411–1438](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/blob/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b/Complete_Affine_Jets_Supplement.tex#L1411-L1438). | Certificate description; no fresh execution. |

The supplement refers to accompanying `certificates/` JSON files, manifests, and verification scripts. These files are absent from the [checked manuscript repository tree](https://github.com/jaehwoo/3-dimensional-Tarry-s-problem/tree/3e95a6b26cf3ff42b8b5bbee1fc3ae73de70d24b); the references are not links to a runnable certificate package in this repository. The supplement, including its certificates, still awaits verification and final revision.

## 5. Which lower bound comes from established literature?

Cheng Bi and Ruichen Sun, [*L^p integrability of functions with Fourier support on High codimension manifolds*](https://arxiv.org/abs/2610.39739v1), arXiv:2610.39739v1 (29 October 2026).

For $n,k\ge2$, their **Theorem 1.1** states that an $L^p(\mathbb R^{N_{n,k}})$ function with Fourier support on the $n$-dimensional Parsell–Vinogradov manifold must vanish when $1\le p<n+\binom{n+k}{n+1}$, where $N_{n,k}=\binom{n+k}{k}-1$. Their **Corollary 1.2** gives

$$
p^{\mathrm{Tar}}_{n,k}\ge n+\binom{n+k}{n+1}\quad(n\ge1,\ k\ge2).
$$

For $n=3$, this is the established lower bound $p^{\mathrm{Tar}}_{3,k}\ge3+\chi_k$. [Source: Theorem 1.1 and Section 1.2, Corollary 1.2](https://arxiv.org/html/2610.39739v1).

**Status:** external literature result, available as an arXiv preprint; no journal-acceptance claim or independent proof audit here. Its strict subcritical nonintegrability statement does not supply endpoint divergence. The matching upper bounds and endpoint arguments indexed above remain claims of these working manuscripts.

## 6. How should verification status be read?

The [public Lean source archive](https://github.com/jaehwoo/Tarry-problem-lean-checkpoint-backup/blob/6714b11056f950c6f662df0f296a8e1076c6eba2/formalization/README.md#L1-L9) describes **557 saved modules** with provenance. Publication of those sources is archival.

| Evidence | Meaning in this index |
| --- | --- |
| Manuscript statement | The stated claim and source location were checked; its proof was not thereby verified. |
| Conditional Lean theorem | A declaration has explicit hypotheses; its mathematical scope is limited to those hypotheses and its actual conclusion. |
| Historical report | A saved record of an earlier run, its assumptions, and its unresolved obligations; not a fresh check of the current sources. |
| Fresh compilation | No Lean compilation, certificate execution, or new axiom audit was performed for this index. |
| Full manuscript verification | Not established by this index or by the module count; complete verification remains pending. |

This index provides navigation for researchers and search tools. It does not guarantee indexing or retrieval by any external LLM.
