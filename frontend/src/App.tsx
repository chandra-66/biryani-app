const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-red-50 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full rounded-3xl bg-white shadow-xl ring-1 ring-slate-200 p-8">
        <p className="text-sm uppercase tracking-[0.2em] text-orange-500 font-semibold">Biryani App</p>
        <h1 className="mt-4 text-4xl font-extrabold text-slate-900">Fresh biryani, delivered fast.</h1>
        <p className="mt-4 text-slate-600 text-lg">
          Frontend setup is ready for Vite + React + TypeScript + Tailwind. Connect this UI to the FastAPI backend and deploy with Vercel.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl bg-orange-50 p-4">
            <p className="text-sm text-slate-500">Customers</p>
            <p className="mt-2 text-2xl font-bold text-orange-600">Orders</p>
          </div>
          <div className="rounded-2xl bg-amber-50 p-4">
            <p className="text-sm text-slate-500">Restaurants</p>
            <p className="mt-2 text-2xl font-bold text-amber-600">Menus</p>
          </div>
          <div className="rounded-2xl bg-red-50 p-4">
            <p className="text-sm text-slate-500">Operations</p>
            <p className="mt-2 text-2xl font-bold text-red-600">Delivery</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
