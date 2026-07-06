# Spec: 用户登录功能

## Why
用户需要登录才能访问个人数据。

## Scope
**In scope:**
- 邮箱+密码登录
- JWT token 签发

**Out of scope:**
- OAuth 第三方登录
- 密码找回

## Technical
- POST /api/login 接口
- bcrypt 密码校验

## Files
- src/auth/login.ts
- src/auth/jwt.ts
- tests/auth/login.test.ts
