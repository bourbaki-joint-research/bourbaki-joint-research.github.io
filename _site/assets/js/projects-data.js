window.BOURBAKI_PROJECTS = [
  {
    "identifier": "2026.01",
    "team": "T1",
    "title": "Prediction of pKa from Molecular Structure",
    "title_en": "",
    "authors": ["김은호","박가온","이제형"],
    "subjects": ["physics.chem-ph","physics.comp-ph","cs.LG"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=18dXLU4QlpfI_trzRxFZP3THu7epIY-p3",
    "submitted": "2026-08-16T18:55:04",
    "url": "/abs/2026.01/",
    "abstract": "The acid dissociation constant is a key physicochemical property governing the solubility and membrane permeability of drugs, yet experimental determination of \\(\\mathrm{p}K_\\mathrm{a}\\) for every molecule of interest is inherently limited. This study aims to predict \\(\\mathrm{p}K_\\mathrm{a}\\) from molecular structure alone while identifying the interpretable variables that genuinely contribute to the prediction. From the IUPAC Dissociation-Constants database (10,626 unique molecules), approximately 200 molecules were selected under controlled measurement conditions of \\(25\\,^{\\circ}\\mathrm{C}\\) and ionic strength below \\(0.1\\ \\mathrm{M}\\), restricting the compounds to three or four functional-group families so that the \\(\\mathrm{p}K_\\mathrm{a}\\) distribution remains balanced. SMILES strings were standardized and converted into three-dimensional structures using RDKit, and the electronic and steric properties were subsequently computed with xTB. Variables exhibiting high multicollinearity were eliminated through variance inflation factor analysis, and four to five final input variables were selected via ElasticNet regression. Model performance is evaluated by RMSE and MAE, and the selected variables are examined for correspondence with established chemical theory. By constructing an algorithm that demonstrates reliable \\(\\mathrm{p}K_\\mathrm{a}\\) prediction from a small set of interpretable variables, this work is expected to offer economic advantages over experimental measurement."
  },
  {
    "identifier": "2026.02",
    "team": "T2",
    "title": "콜라츠 비자명 주기의 조건",
    "title_en": "Conditions for Nontrivial Cycles of the Collatz Map",
    "authors": ["전지환","유도원","김나겸"],
    "subjects": ["math.NT","cs.DM"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1tObkdCbG51QIwVB6v1b3Taibz_MxueKe",
    "submitted": "2026-08-16T23:50:35",
    "url": "/abs/2026.02/",
    "abstract": "The Collatz conjecture remains unresolved, and a counterexample could be either an unbounded orbit or a nontrivial cycle. This study focuses on necessary arithmetic conditions for nontrivial cycles. By retaining only odd terms, we encode a hypothetical cycle as a positive integer exponent vector. Iterating the odd-only Syracuse map yields the closure equation \\((2^{A}-3^{r})x_{0}=N_{0}(\\mathbf{a})\\). With \\(D=2^{A}-3^{r}\\), integrality requires \\(D&gt;0\\), divisibility of each numerator associated with a cyclic rotation of the vector, and the prescribed exact powers of \\(2\\) at every step. We express these numerators in Horner form to update only modular remainders. For a prime-power divisor \\(q^{e}\\) of \\(D\\), we construct a dynamic-programming state that records the number of selected exponents, their partial sum, and the current Horner remainder modulo \\(q^{e}\\). Partial vectors reaching the same state are merged. If the required zero remainder is unreachable, the corresponding family is excluded. Expected outcomes include finite-range modular exclusion criteria, quantified reductions in candidate counts and running time relative to exhaustive enumeration, and reproducible computational certificates with open code. This study does not claim a proof of the Collatz conjecture; it instead aims to provide transparent tools for eliminating structured families of hypothetical cycles."
  },
  {
    "identifier": "2026.03",
    "team": "T3",
    "title": "Structural Variations of Weyl Algebras by Characteristic and the Investigation of Modern Open Problems",
    "title_en": "",
    "authors": ["류호인","서윤서","홍태원","나윤오"],
    "subjects": ["math.RA","math.AG"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1xEP_DdcBZSN00nD0Nrxuwlc9YSQPJkDC",
    "submitted": "2026-08-19T23:55:07",
    "url": "/abs/2026.03/",
    "abstract": "This study analyzes the Weyl algebra \\(A_{1}=\\langle x,\\partial \\mid \\partial x-x\\partial =1\\rangle\\), the algebraic structure behind the Heisenberg uncertainty relation, and shows how its representation theory and center change with the characteristic of the base field. In characteristic \\(0\\), a trace argument proves that \\(A_{1}\\) has no finite-dimensional matrix representation: if \\(AB-BA=I_{n}\\), then \\(\\operatorname{Tr}(AB)-\\operatorname{Tr}(BA)=0\\), while \\(\\operatorname{Tr}(I_{n})=n\\), forcing \\(n=0\\), a contradiction. The center of \\(A_{1}\\) is then just the scalars. In characteristic \\(p\\), this obstruction vanishes since \\(\\operatorname{Tr}(I_{p})=p\\equiv 0 \\pmod{p}\\), and we construct an explicit \\(3\\times 3\\) representation over \\(\\mathbb{F}_{3}\\) verifying \\(DX-XD=I_{3}\\). We also show \\(x^{p}\\) and \\(\\partial^{p}\\) become central, expanding the center to \\(\\mathbb{F}_{p}[x^{p},\\partial^{p}]\\). We link this to the Jacobian conjecture. It remains open in characteristic \\(0\\), but in characteristic \\(p\\) we give a counterexample: \\(f(x)=x-x^{p}\\) satisfies \\(f^{\\prime}(x)=1\\) yet is not injective, by Fermat’s little theorem. Finally, we discuss how the enlarged center in characteristic \\(p\\) bridges the Dixmier conjecture and the Jacobian conjecture, linking operator algebra and algebraic geometry."
  },
  {
    "identifier": "2026.04",
    "team": "T4",
    "title": "A Ramsey-Theoretic Approach to the Erdős–Szekeres convex polygon Theorem",
    "title_en": "",
    "authors": ["오여준","지연우","박시유","정희범"],
    "subjects": ["math.CO","math.MG"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1-RajzIqu1h3DafiN3hO3BhYZEBB5d0wo",
    "submitted": "2026-08-20T00:17:18",
    "url": "/abs/2026.04/",
    "abstract": "The Erdős–Szekeres convex polygon theorem states that for any positive integer \\(N\\), every sufficiently large finite set of points in general position in the plane contains a subset of \\(N\\) points that form a convex \\(N\\)-gon. This study proves the Erdős–Szekeres convex polygon theorem from the perspective of Ramsey theory, compares it with geometric proofs, and analyzes its efficiency, including the upper bound on the number of points, while exploring possibilities for improvement and seeking a novel proof. In particular, we verify the existence of a convex \\(n\\)-gon using \\(R_4(n, 5)\\) and subsequently investigate proofs that enhance efficiency by employing other Ramsey numbers. This research holds significance in analyzing and advancing the limitations of existing proofs, thereby contributing to a deeper understanding of the interplay between geometry and combinatorics."
  },
  {
    "identifier": "2026.05",
    "team": "T5",
    "title": "Realizability of Monomial Forms in Multivariable Polynomial Invariants of Virtual Knots",
    "title_en": "",
    "authors": ["정우혁","이정윤","김민혁"],
    "subjects": ["math.GT","math.CO"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1d4U_ogJU82AbT9o_aOTTVj9gDqo0NWJ5",
    "submitted": "2026-08-16T20:53:01",
    "url": "/abs/2026.05/",
    "abstract": "The multivariable polynomial \\(M_D(x_0, \\dots, x_n)\\) extends the affine index polynomial \\(P_K(t)\\) for virtual knots, yet its realizable algebraic forms remain strictly constrained. Using Gauss diagram analysis, we derive a global parity condition on chord intersections to investigate the realizability of monomial forms. Consequently, we demonstrate that single-monomial forms are generally unrealizable, proving that the polynomial structure of \\(M_D\\) is globally restricted by the chord intersection topology."
  },
  {
    "identifier": "2026.06",
    "team": "T6",
    "title": "An Analysis of Optimal Two-Shortcut Placement in Cycle Networks as a Function of Network Size",
    "title_en": "",
    "authors": ["조정완","신우석","천다예"],
    "subjects": ["math.CO","cs.DM"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1PeqapkgHd0wZ2mkOYU508Siviy0t0v7S",
    "submitted": "2026-08-20T19:42:15",
    "url": "/abs/2026.06/",
    "abstract": "A cycle graph offers two routes between vertices but may require long paths between distant pairs. Adding shortcut edges can reduce these distances, yet the best placement of two shortcuts is not obvious because improving a few pairs need not minimize the average over all pairs. This study will determine how two unit-length shortcut edges should be placed in an unweighted cycle graph \\(C_{n}\\) to minimize average shortest-path length. We will calculate small cases by hand to validate an exhaustive-search program. For each \\(n\\), the program will enumerate admissible pairs of shortcuts, compute all-pairs distances by breadth-first search, and classify optimal configurations as shared-endpoint, crossing, or noncrossing. Cases with \\(6\\le n\\le 30\\) will be used to identify patterns in endpoint gaps and configuration types, while additional cases up to \\(n=50\\) will test the resulting conjectures. We expect to determine optimal placements in the investigated range, identify recurring structural features, formulate a conjectural rule for arbitrary \\(n\\), and produce a verified search program. Where feasible, partial results will be proved using rotational and reflection symmetries. This study combines computational exploration with mathematical reasoning to characterize efficient link placement."
  },
  {
    "identifier": "2026.07",
    "team": "T7",
    "title": "최단 초순열 탐색 알고리즘 설계",
    "title_en": "Design of a Search Algorithm for Shortest Superpermutations",
    "authors": ["유예준","임지수","김시헌","김종하"],
    "subjects": ["cs.DS","math.CO"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1rG24Ve-LzpF_xa5xAJ9WtkqCwPk-Puvo",
    "submitted": "2026-08-16T16:37:31",
    "url": "/abs/2026.07/",
    "abstract": "A superpermutation is a string that contains all \\(n!\\) permutations of \\(n\\) symbols as contiguous substrings. Finding the shortest superpermutation is difficult because the search space grows rapidly as \\(n\\) increases, making exhaustive search impractical for larger values of \\(n\\). This study proposes a heuristic algorithm for constructing short superpermutations under limited computational time. Unlike conventional permutation-level approaches, which select the next permutation to append, our method expands the string one character at a time and checks whether each newly formed length-\\(n\\) substring produces an uncovered permutation. To guide character selection, we introduce a deficit-based scoring function that rewards the creation of new permutations and underrepresented patterns while penalizing repeated coverage and poor future expandability. We further combine this score with Monte Carlo simulations to estimate the long-term effectiveness of each candidate character. After the fast coverage stage, remaining uncovered permutations are inserted through a patching process, followed by compression and independent output validation. The proposed algorithm will be compared with randomized greedy search, beam search, and local-search-based methods using minimum length, average length, median, standard deviation, runtime, and gap from the known lower bound. This study aims to evaluate whether character-level heuristic exploration can generate shorter superpermutation candidates more efficiently than existing heuristic baselines."
  },
  {
    "identifier": "2026.08",
    "team": "T8",
    "title": "The Random-Walk Behavior of the Partial Sums of the Möbius Function (Mertens Function) and a Probabilistic Interpretation of the Riemann Zeta Function",
    "title_en": "",
    "authors": ["이서우","신지묵","심규호","이주영"],
    "subjects": ["math.NT","math.PR"],
    "comments": "Interim presentation, 2026 Bourbaki Joint Research Project",
    "slides_url": "https://drive.google.com/open?id=1BAZxiIhMdSsxvR-8uX01PkYPQSXbLLeS",
    "submitted": "2026-08-16T23:51:47",
    "url": "/abs/2026.08/",
    "abstract": "The Möbius function \\(\\mu(n)\\) and its summatory function, the Mertens function \\(M(x)=\\sum_{n\\le x}\\mu(n)\\), are linked to the Riemann zeta function via \\(1/\\zeta(s)=\\sum_{n=1}^{\\infty}\\mu(n)/n^{s}\\); indeed, the Riemann Hypothesis is equivalent to \\(M(x)=O(x^{1/2+\\varepsilon})\\). Motivated by this, we model \\(\\mu(n)\\) as a quasi-random sequence and investigate whether the normalized function \\(M(x)/\\sqrt{x}\\) behaves like a simple random walk. Using Perron’s formula and Cauchy’s integral theorem, we relate this probabilistic behavior to the distribution of zeta zeros. We examine the statistical independence of \\(\\mu(n)\\) via autocorrelation (Chowla’s conjecture), test the approximate normality of \\(M(x)/\\sqrt{x}\\) using the Kolmogorov–Smirnov statistic, and compare \\(M(x)\\) against simulated random walks, supported by numerical computations for \\(n\\le 10^{7}\\). Rather than proving or disproving RH, this study aims to numerically assess how closely the behavior of \\(M(x)\\) aligns with random-walk predictions."
  }
];
window.BOURBAKI_CATS = {"math.NT":{"archive":"Mathematics","name":"Number Theory"},"math.CO":{"archive":"Mathematics","name":"Combinatorics"},"math.RA":{"archive":"Mathematics","name":"Rings and Algebras"},"math.AG":{"archive":"Mathematics","name":"Algebraic Geometry"},"math.GT":{"archive":"Mathematics","name":"Geometric Topology"},"math.MG":{"archive":"Mathematics","name":"Metric Geometry"},"math.PR":{"archive":"Mathematics","name":"Probability"},"math.AT":{"archive":"Mathematics","name":"Algebraic Topology"},"math.DS":{"archive":"Mathematics","name":"Dynamical Systems"},"math.LO":{"archive":"Mathematics","name":"Logic"},"cs.DS":{"archive":"Computer Science","name":"Data Structures and Algorithms"},"cs.DM":{"archive":"Computer Science","name":"Discrete Mathematics"},"cs.LG":{"archive":"Computer Science","name":"Machine Learning"},"cs.CC":{"archive":"Computer Science","name":"Computational Complexity"},"physics.chem-ph":{"archive":"Physics","name":"Chemical Physics"},"physics.comp-ph":{"archive":"Physics","name":"Computational Physics"},"q-bio.QM":{"archive":"Quantitative Biology","name":"Quantitative Methods"},"stat.ML":{"archive":"Statistics","name":"Machine Learning"}};
window.BOURBAKI_BASE = "";
window.BOURBAKI_ID_PREFIX = "Bourbaki";
