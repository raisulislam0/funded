# 🎨 Frontend Plan - Funded Bangladesh

## 📋 Overview

Next.js 14 frontend with App Router, TypeScript, TailwindCSS, and shadcn/ui.

## 🏗️ Proposed Structure

```
frontend/
├── src/
│   ├── app/                          # Next.js 14 App Router
│   │   ├── (auth)/                   # Auth layout group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (main)/                   # Main layout group
│   │   │   ├── layout.tsx            # Main layout with header/footer
│   │   │   ├── page.tsx              # Home page
│   │   │   │
│   │   │   ├── campaigns/
│   │   │   │   ├── page.tsx          # Campaign listing
│   │   │   │   ├── [slug]/
│   │   │   │   │   └── page.tsx      # Campaign details
│   │   │   │   └── create/
│   │   │   │       └── page.tsx      # Create campaign
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── donor/
│   │   │   │   │   └── page.tsx      # Donor dashboard
│   │   │   │   └── creator/
│   │   │   │       └── page.tsx      # Creator dashboard
│   │   │   │
│   │   │   └── profile/
│   │   │       └── page.tsx          # User profile
│   │   │
│   │   ├── (admin)/                  # Admin layout group
│   │   │   ├── layout.tsx
│   │   │   └── admin/
│   │   │       ├── page.tsx          # Admin dashboard
│   │   │       ├── campaigns/
│   │   │       ├── users/
│   │   │       └── withdrawals/
│   │   │
│   │   ├── layout.tsx                # Root layout
│   │   ├── globals.css               # Global styles
│   │   └── api/                      # API routes (if needed)
│   │
│   ├── components/
│   │   ├── ui/                       # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   │
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Navigation.tsx
│   │   │
│   │   ├── campaigns/
│   │   │   ├── CampaignCard.tsx
│   │   │   ├── CampaignGrid.tsx
│   │   │   ├── CampaignDetails.tsx
│   │   │   ├── CampaignProgress.tsx
│   │   │   ├── DonationForm.tsx
│   │   │   └── CreateCampaignForm.tsx
│   │   │
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   │
│   │   └── common/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorMessage.tsx
│   │       ├── Pagination.tsx
│   │       └── SearchBar.tsx
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts             # Axios/fetch wrapper
│   │   │   ├── auth.ts               # Auth API calls
│   │   │   ├── campaigns.ts          # Campaign API calls
│   │   │   ├── donations.ts          # Donation API calls
│   │   │   └── users.ts              # User API calls
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts            # Auth hook
│   │   │   ├── useCampaigns.ts       # Campaigns hook
│   │   │   ├── useDonations.ts       # Donations hook
│   │   │   └── useUser.ts            # User hook
│   │   │
│   │   ├── context/
│   │   │   ├── AuthContext.tsx       # Auth context
│   │   │   └── ThemeContext.tsx      # Theme context
│   │   │
│   │   ├── utils/
│   │   │   ├── format.ts             # Formatting utilities
│   │   │   ├── validation.ts         # Validation schemas
│   │   │   └── constants.ts          # Constants
│   │   │
│   │   └── types/
│   │       ├── auth.ts               # Auth types
│   │       ├── campaign.ts           # Campaign types
│   │       ├── donation.ts           # Donation types
│   │       └── user.ts               # User types
│   │
│   └── styles/
│       └── globals.css               # Global styles
│
├── public/
│   ├── images/
│   ├── icons/
│   └── favicon.ico
│
├── .env.local                        # Environment variables
├── .env.example                      # Environment template
├── next.config.js                    # Next.js config
├── tailwind.config.ts                # Tailwind config
├── tsconfig.json                     # TypeScript config
├── package.json                      # Dependencies
└── README.md                         # Frontend docs
```

## 📦 Dependencies

### Core
```json
{
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.3"
  }
}
```

### UI & Styling
```json
{
  "dependencies": {
    "tailwindcss": "^3.4.1",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1",
    "lucide-react": "^0.316.0"
  }
}
```

### Forms & Validation
```json
{
  "dependencies": {
    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.4"
  }
}
```

### API & State
```json
{
  "dependencies": {
    "axios": "^1.6.5",
    "@tanstack/react-query": "^5.17.19",
    "zustand": "^4.5.0"
  }
}
```

### Utilities
```json
{
  "dependencies": {
    "date-fns": "^3.2.0",
    "react-hot-toast": "^2.4.1",
    "sharp": "^0.33.2"
  }
}
```

### Dev Dependencies
```json
{
  "devDependencies": {
    "@types/node": "^20.11.5",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0",
    "prettier": "^3.2.4",
    "prettier-plugin-tailwindcss": "^0.5.11"
  }
}
```

## 🎨 Key Pages

### 1. Home Page (`/`)
**Features:**
- Hero section with CTA
- Featured campaigns
- Campaign categories
- Statistics (total raised, campaigns, donors)
- How it works section
- Testimonials

**Components:**
- `Hero.tsx`
- `FeaturedCampaigns.tsx`
- `CategoryGrid.tsx`
- `Statistics.tsx`
- `HowItWorks.tsx`

### 2. Campaign Listing (`/campaigns`)
**Features:**
- Grid/List view toggle
- Filters (category, status, location)
- Search functionality
- Sorting options
- Pagination
- Campaign cards with progress

**Components:**
- `CampaignGrid.tsx`
- `CampaignFilters.tsx`
- `SearchBar.tsx`
- `CampaignCard.tsx`

### 3. Campaign Details (`/campaigns/[slug]`)
**Features:**
- Campaign information
- Progress bar
- Image gallery
- Campaign updates
- Comments section
- Donation form
- Share buttons
- Creator profile

**Components:**
- `CampaignHeader.tsx`
- `CampaignProgress.tsx`
- `ImageGallery.tsx`
- `DonationForm.tsx`
- `UpdatesList.tsx`
- `CommentsList.tsx`

### 4. Create Campaign (`/campaigns/create`)
**Features:**
- Multi-step form wizard
- Image upload with preview
- Document upload
- Form validation
- Draft saving
- Preview before submit

**Components:**
- `CreateCampaignWizard.tsx`
- `BasicInfoStep.tsx`
- `MediaStep.tsx`
- `DocumentsStep.tsx`
- `ReviewStep.tsx`

### 5. Login/Register (`/login`, `/register`)
**Features:**
- Email/password authentication
- Form validation
- Error handling
- Redirect after login
- Remember me option

**Components:**
- `LoginForm.tsx`
- `RegisterForm.tsx`
- `AuthLayout.tsx`

### 6. Donor Dashboard (`/dashboard/donor`)
**Features:**
- Donation history
- Favorite campaigns
- Badges earned
- Total donated
- Impact statistics

**Components:**
- `DonationHistory.tsx`
- `FavoriteCampaigns.tsx`
- `BadgesList.tsx`
- `ImpactStats.tsx`

### 7. Creator Dashboard (`/dashboard/creator`)
**Features:**
- My campaigns
- Campaign analytics
- Withdrawal requests
- Campaign updates
- Donor list

**Components:**
- `MyCampaigns.tsx`
- `CampaignAnalytics.tsx`
- `WithdrawalRequests.tsx`
- `DonorList.tsx`

### 8. Admin Dashboard (`/admin`)
**Features:**
- Campaign review queue
- User verification queue
- Withdrawal approvals
- Transaction monitoring
- User management

**Components:**
- `ReviewQueue.tsx`
- `VerificationQueue.tsx`
- `WithdrawalApprovals.tsx`
- `TransactionMonitor.tsx`

## 🔐 Authentication Flow

### JWT Token Management
```typescript
// lib/auth/tokens.ts
export const setTokens = (access: string, refresh: string) => {
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
};

export const getAccessToken = () => localStorage.getItem('accessToken');
export const getRefreshToken = () => localStorage.getItem('refreshToken');

export const clearTokens = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};
```

### API Client with Auto-Refresh
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Try to refresh token
      const refreshToken = getRefreshToken();
      if (refreshToken) {
        try {
          const { data } = await axios.post('/api/v1/accounts/token/refresh/', {
            refresh: refreshToken,
          });
          setTokens(data.access, refreshToken);
          error.config.headers.Authorization = `Bearer ${data.access}`;
          return axios(error.config);
        } catch {
          clearTokens();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
```

## 🎯 Implementation Steps

### Phase 1: Setup (Week 1)
1. Initialize Next.js project with TypeScript
2. Install and configure TailwindCSS
3. Set up shadcn/ui
4. Configure ESLint and Prettier
5. Set up folder structure
6. Create environment variables

### Phase 2: Core Features (Week 2-3)
1. Implement authentication
2. Create layout components
3. Build home page
4. Implement campaign listing
5. Create campaign details page

### Phase 3: User Features (Week 4-5)
1. Donation flow
2. Campaign creation wizard
3. User dashboards
4. Profile management
5. Verification flow

### Phase 4: Admin & Polish (Week 6)
1. Admin dashboard
2. Review queues
3. Analytics
4. Error handling
5. Loading states
6. Responsive design

### Phase 5: Testing & Optimization (Week 7)
1. Unit tests
2. Integration tests
3. E2E tests
4. Performance optimization
5. SEO optimization
6. Accessibility

## 🚀 Commands to Initialize

```bash
# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app --src-dir

# Install shadcn/ui
npx shadcn-ui@latest init

# Install dependencies
cd frontend
npm install axios @tanstack/react-query react-hook-form zod @hookform/resolvers
npm install date-fns react-hot-toast
npm install lucide-react class-variance-authority clsx tailwind-merge

# Install shadcn components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add select
npx shadcn-ui@latest add form
npx shadcn-ui@latest add toast

# Run development server
npm run dev
```

## 📝 Next Steps

After backend is confirmed working:
1. Ask for permission to initialize frontend
2. Create Next.js project structure
3. Set up authentication
4. Build core pages
5. Integrate with backend API
6. Test end-to-end flow

---

**Ready to build the frontend when you are!** 🚀

