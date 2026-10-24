# Sessions and tokens

Last reviewed: 2026-10-24

A concept page: how a system remembers who you are between requests, and why that memory is worth stealing.

## Problem

The web forgets you between requests: each one arrives on its own. Once you've logged in, something has to come with every later request to prove it's still you. Whatever that something is, it works like a password while it lasts, so it can be forged, stolen, and kept after it should have expired.

## The story

In 2006 Ana Lucía Torres built the login for a small online travel agency. After a customer typed their password correctly, the site needed to remember them. Ana Lucía did the simplest thing that worked. She stored the customer's ID in a cookie, `user_id=4182`, which the browser sent back with every request. The site read it and knew who was asking.

A customer reported, a little nervously, that he'd changed the number in his cookie to 4183 out of curiosity and was now looking at a stranger's bookings. Ana Lucía felt her stomach drop. The cookie was on the customer's own machine, and anything on the customer's machine could be edited ([page 6](../06-anyone-can-publish.md)).

Her fix was a random session ID. After login, the server created a long random string, stored it on the server alongside the customer's ID, and sent only the random string to the browser. Nobody could guess another customer's string, and changing it just meant being logged out. It was the standard answer, and she was proud of how quickly she'd fixed it.

In 2010 a programmer released a browser add-on called Firesheep that, on any open café wifi, showed a list of everyone nearby who was logged into popular sites, and let you become them with a click. It didn't break passwords. It just collected session cookies from the air. Ana Lucía's site encrypted the login page, but every later page was plain HTTP, so the session ID crossed the café's network in the open. The random string was impossible to guess and trivial to copy.

*Before reading on: the session ID couldn't be guessed, and it could be copied from the network and used by anyone who had it. What else did it need?*

Ana Lucía made every page HTTPS, not just the login, so session IDs travelled encrypted ([TLS](tls.md)). She marked the cookie so browsers would only send it over encrypted connections and wouldn't let page scripts read it. Sessions now expired after a few hours of inactivity, and changing a password ended every other session the customer had open. And she gave the token less power. A session could view and change bookings, but taking payment or changing the account's email address required the password again.

Looking back, Ana Lucía thought she'd learned that a token is a password with a shorter life. It has to be unguessable, kept secret in transit and in the browser, limited in what it can do, and possible to cancel.

## Where it shows up

| Page | The token | What it needed |
| --- | --- | --- |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | What proves who you are after the password's been checked | The same care as the password, because it works like one. |
| [TLS](tls.md) | Session cookies crossing a network | Encryption on every request, not just the login. |
| [6, Anyone can publish](../06-anyone-can-publish.md) | Anything stored on the client | It can be read and edited by whoever controls the browser. |
| [Least privilege](least-privilege.md) | What a token is allowed to do | Less power, so a stolen token does less harm. |

It shows up elsewhere too: API keys, "remember me" cookies, password reset links, mobile app tokens, and the credentials one service uses to call another.

What these share is that anything that grants access while it exists is a password in all but name: keep it secret, keep it short-lived, keep it narrow, and keep a way to revoke it.

## It really happened

Ana Lucía is fictional; Firesheep was real. Eric Butler released it in October 2010 to show that many large sites, including Facebook and Twitter, encrypted only the login and sent session cookies unencrypted afterwards ([Butler's announcement](https://codebutler.com/2010/10/24/firesheep/)). Within a few years, encrypting every page became the norm for major sites. Signed tokens that carry their own claims, such as JSON Web Tokens (standardised in 2015), let servers check a token without looking it up. That makes them harder to revoke early, which is why they're usually kept short-lived.

## What it is

A session is the server's memory that a client has authenticated; a token is what the client presents to prove it. Tokens are either references, a random ID looked up on the server, or self-contained, signed data the server can verify on its own. Either way, they must be unguessable, sent only over encrypted connections, stored where scripts and other sites can't reach them, scoped to what's needed, and expired or revocable.

## Where it gets misapplied

- **Identity the client can edit.** Ana Lucía's `user_id=4182`.
- **Encrypting only the login.** The token that follows is as valuable as the password.
- **Long-lived tokens with no way to revoke them.** A stolen laptop that stays logged in for a year.
- **The mirror:** logging people out every ten minutes. Security that drives users to save passwords in a text file is worse than a sensible session length.

## Connections

- Learning this is also learning [TLS](tls.md), because a token is only secret if it travels encrypted.
- Learning this is also learning [password storage](password-storage.md), because the password check is what the token stands in for afterwards.
- Learning this is also learning [least privilege](least-privilege.md), because a token should carry no more power than its job needs.
- Learning this is also learning [input validation](input-validation.md), because a token is input from the client, and the server must check it every time.
- Learning this is also learning [cloud IAM](cloud-iam.md), because cloud credentials are tokens for machines, with the same rules.

## Resources

1. [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) (start here: the practical rules). <!-- verify -->
2. Eric Butler, ["Firesheep"](https://codebutler.com/2010/10/24/firesheep/) (2010) (go deeper: a short post that changed the web).
3. RFC 7519, JSON Web Token (reference). <!-- verify -->

## Names you'll hear

- **Session, session ID:** the server's record of a login, and the random string that points to it.
- **Cookie:** data the browser stores and sends back automatically.
- **Session hijacking:** stealing and using someone's session token.
- **JWT:** a signed, self-contained token.
- **Secure, HttpOnly, SameSite:** cookie settings limiting when it's sent and who can read it.
- **Refresh token:** a longer-lived token used only to get new short-lived ones.

## Go and look

Log into a site you use, open the browser's developer tools, and find its session cookie. Check its settings: does it expire, is it marked secure, can scripts read it?
