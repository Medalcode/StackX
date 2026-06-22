FROM node:18-alpine AS deps
WORKDIR /app
COPY frontend/package.json /app/package.json
RUN npm install

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules /app/node_modules
COPY frontend /app
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=http://backend:8000
COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/public /app/public
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/node_modules /app/node_modules
EXPOSE 3000
CMD ["npm", "run", "start"]
