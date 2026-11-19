# Security

Last reviewed: 2026-11-19

A family index. Keeping each person's data their own and each program within its power, against people who are trying. Four of its pages, from symmetric encryption to randomness, are the cryptography inside the rest, and read best together and in order.

## In reading order

In the order the spine first needs them, with pages that lean on each other kept together.

1. [Multi-tenancy](multi-tenancy.md): many customers sharing one system, and the boundary that must keep each one's data their own. First needed on [page 4](../04-data-outlives-programs.md).
2. [TLS](tls.md): how two machines that have never met agree on a secret, and prove who they are, over a network anyone can read. First needed on [page 5](../05-machines-need-to-talk.md).
3. [Input validation](input-validation.md): why input from outside must be treated as data, never as instructions. First needed on [page 6](../06-anyone-can-publish.md).
4. [Least privilege](least-privilege.md): give every person and program only the power it needs. First needed on [page 7](../07-strangers-on-the-network.md).
5. [Sessions and tokens](sessions-and-tokens.md): how a system remembers who you are between requests, and why that memory is worth stealing. First needed on [page 7](../07-strangers-on-the-network.md).
6. [Password storage](password-storage.md): storing something you can check but never read, and keeping it that way as attackers get faster. First needed on [page 7](../07-strangers-on-the-network.md).
7. [Symmetric encryption](symmetric-encryption.md): one shared key that locks and unlocks, the fastest way to protect data from someone who can see it, and the easiest to use in a way that quietly gives the secret away. First needed on [page 7](../07-strangers-on-the-network.md).
8. [Public-key cryptography](public-key.md): how two parties who have never met can agree on a secret over a channel anyone can read, and how anyone can check who signed something, without either side ever sending a secret. First needed on [page 7](../07-strangers-on-the-network.md).
9. [Key management](key-management.md): where keys live, who and what can use them, how they're replaced, and what you do on the day one leaks. First needed on [page 7](../07-strangers-on-the-network.md).
10. [Randomness](randomness.md): every key, nonce and token is only as secret as the randomness it came from, and a computer is a machine built not to be random. First needed on [page 7](../07-strangers-on-the-network.md).
11. [Software supply chain](supply-chain.md): the code you didn't write, written by people you've never met, running with all the power of the code you did. First needed on [page 7](../07-strangers-on-the-network.md).
12. [Cloud IAM](cloud-iam.md): who and what may do which actions on which resources in a cloud account, and why a leaked key can cost a fortune overnight. First needed on [page 9](../09-buying-computers-is-too-slow.md).
13. [Code signing](code-signing.md): proving who made a piece of software, and that nobody changed it on the way, and what that proof doesn't cover. First needed on [page 10](../10-many-people-one-codebase.md).
