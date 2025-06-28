### New Development Plan

**Objective:** To build a reliable and user-friendly water quality application that provides a clear "safe to drink" status based on a user's location or search query, and to fix all existing bugs.

---

### Phase 1: Bug Fixes & Core Functionality Refinement

**Goal:** To create a stable and bug-free foundation before adding new features.

1.  **Fix `pwsid` is `undefined` Bug:**
    *   **Problem:** The `pwsid` is not being correctly passed from the `HomePage` to the `WaterSystemReport` page.
    *   **Solution:** Carefully re-examine the `Link` component in `HomePage.tsx` and the `useParams` hook in `WaterSystemReport.tsx` to ensure the `pwsid` is being correctly passed and received.

2.  **Fix Zip Code Search:**
    *   **Problem:** The search functionality is not returning results for zip codes.
    *   **Solution:** Investigate the `search_systems` function in `crud.py` and the corresponding API endpoint. Test the endpoint directly to see if the issue is in the backend query or the frontend's handling of the search term.

---

### Phase 2: Location-Based "Safe to Drink" Status

**Goal:** To provide an immediate, location-aware assessment of water quality on the home page.

1.  **Backend Enhancements:**
    *   **New Endpoint:** Create a new endpoint, `/api/systems/by-location`, that accepts latitude and longitude coordinates.
    *   **Spatial Query:** This endpoint will perform a spatial query on the `sdwa_geographic_areas` table to find the nearest water system to the user's location.
    *   **Status Check:** Once the nearest system is identified, the endpoint will use the existing `get_water_system_status` function to determine if the water is safe to drink.

2.  **Frontend Implementation:**
    *   **Geolocation:** Implement a function on the `HomePage` that requests the user's permission to access their location using the browser's `navigator.geolocation` API.
    *   **"Safe to Drink" Component:** Create a new component that displays the "safe to drink" status prominently on the home page. This component will call the new `/api/systems/by-location` endpoint to get the status for the user's current location.

---

### Phase 3: Home Page Statistics

**Goal:** To create a more informative and engaging home page with high-level statistics.

1.  **Backend:** The `/statistics` endpoint is already created, so no new backend work is needed for this phase.
2.  **Frontend:** Implement the UI components on the `HomePage` to display the statistics fetched from the `/statistics` endpoint.
