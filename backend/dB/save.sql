-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.units (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  branch text,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  CONSTRAINT units_pkey PRIMARY KEY (id)
);
CREATE TABLE public.users (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  unit_id uuid,
  first_name text NOT NULL,
  last_name text NOT NULL,
  role text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  CONSTRAINT users_pkey PRIMARY KEY (id),
  CONSTRAINT users_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id)
);
CREATE TABLE public.camps (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  unit_id uuid,
  name text NOT NULL,
  location text,
  start_date timestamp with time zone,
  end_date timestamp with time zone,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  unit_name text,
  CONSTRAINT camps_pkey PRIMARY KEY (id),
  CONSTRAINT camps_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id)
);
CREATE TABLE public.camp_presences (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  camp_id uuid,
  user_id uuid,
  status text DEFAULT 'present'::text,
  CONSTRAINT camp_presences_pkey PRIMARY KEY (id),
  CONSTRAINT camp_presences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id),
  CONSTRAINT camp_presences_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.camps(id)
);
CREATE TABLE public.activities (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  title text NOT NULL,
  duration_minutes integer,
  imaginary_and_objectives text,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  CONSTRAINT activities_pkey PRIMARY KEY (id)
);
CREATE TABLE public.planning_slots (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  camp_id uuid,
  activity_id uuid,
  start_time timestamp with time zone NOT NULL,
  end_time timestamp with time zone NOT NULL,
  title text NOT NULL,
  slot_type text NOT NULL,
  CONSTRAINT planning_slots_pkey PRIMARY KEY (id),
  CONSTRAINT planning_slots_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id),
  CONSTRAINT planning_slots_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.camps(id)
);
CREATE TABLE public.activity_steps (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  activity_id uuid,
  start_time text,
  duration_minutes integer,
  title text NOT NULL,
  description text,
  order_index integer NOT NULL,
  CONSTRAINT activity_steps_pkey PRIMARY KEY (id),
  CONSTRAINT activity_steps_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id)
);
CREATE TABLE public.activity_materials (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  activity_id uuid,
  item_name text NOT NULL,
  is_checked boolean DEFAULT false,
  CONSTRAINT activity_materials_pkey PRIMARY KEY (id),
  CONSTRAINT activity_materials_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id)
);
CREATE TABLE public.activity_responsibles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  activity_id uuid,
  adherent_id text,
  CONSTRAINT activity_responsibles_pkey PRIMARY KEY (id),
  CONSTRAINT activity_responsibles_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id)
);
CREATE TABLE public.ingredients (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  category text NOT NULL,
  unit_type text NOT NULL,
  CONSTRAINT ingredients_pkey PRIMARY KEY (id)
);
CREATE TABLE public.recipes (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  dish_type text NOT NULL,
  instructions text,
  is_vegetarian boolean DEFAULT false,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  is_fridge_free boolean DEFAULT false,
  is_wood_fire boolean DEFAULT false,
  CONSTRAINT recipes_pkey PRIMARY KEY (id)
);
CREATE TABLE public.recipe_ingredients (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  recipe_id uuid,
  ingredient_id uuid,
  qty_child numeric NOT NULL,
  qty_adult numeric NOT NULL,
  CONSTRAINT recipe_ingredients_pkey PRIMARY KEY (id),
  CONSTRAINT recipe_ingredients_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id),
  CONSTRAINT recipe_ingredients_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id)
);
CREATE TABLE public.meals (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  planning_slot_id uuid,
  additional_guests integer DEFAULT 0,
  CONSTRAINT meals_pkey PRIMARY KEY (id),
  CONSTRAINT meals_planning_slot_id_fkey FOREIGN KEY (planning_slot_id) REFERENCES public.planning_slots(id)
);
CREATE TABLE public.meal_recipes (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  meal_id uuid,
  recipe_id uuid,
  CONSTRAINT meal_recipes_pkey PRIMARY KEY (id),
  CONSTRAINT meal_recipes_meal_id_fkey FOREIGN KEY (meal_id) REFERENCES public.meals(id),
  CONSTRAINT meal_recipes_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id)
);
CREATE TABLE public.shopping_lists (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  camp_id uuid,
  ingredient_id uuid,
  total_quantity numeric NOT NULL,
  is_checked boolean DEFAULT false,
  CONSTRAINT shopping_lists_pkey PRIMARY KEY (id),
  CONSTRAINT shopping_lists_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id),
  CONSTRAINT shopping_lists_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.camps(id)
);
CREATE TABLE public.adherent_extras (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  adherent_id character varying NOT NULL,
  photo_url text,
  fiche_url text,
  progression_symbole text,
  progression_action text,
  CONSTRAINT adherent_extras_pkey PRIMARY KEY (id)
);
CREATE TABLE public.chef_mappings (
  email text NOT NULL,
  adherent_id text NOT NULL,
  unit_name text,
  CONSTRAINT chef_mappings_pkey PRIMARY KEY (email)
);
CREATE TABLE public.camp_guests (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  adherent_id text,
  camp_id uuid,
  CONSTRAINT camp_guests_pkey PRIMARY KEY (id),
  CONSTRAINT camp_guests_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.camps(id)
);
CREATE TABLE public.tents (
  id integer NOT NULL DEFAULT nextval('tents_id_seq'::regclass),
  name text NOT NULL,
  capacity integer NOT NULL,
  status text DEFAULT 'operationnelle'::text,
  group_name text,
  CONSTRAINT tents_pkey PRIMARY KEY (id)
);
CREATE TABLE public.camp_tents (
  id integer NOT NULL DEFAULT nextval('camp_tents_id_seq'::regclass),
  camp_id uuid NOT NULL,
  tent_id integer,
  CONSTRAINT camp_tents_pkey PRIMARY KEY (id),
  CONSTRAINT camp_tents_tent_id_fkey FOREIGN KEY (tent_id) REFERENCES public.tents(id)
);
CREATE TABLE public.tent_incidents (
  id integer NOT NULL DEFAULT nextval('tent_incidents_id_seq'::regclass),
  tent_id integer,
  camp_id uuid,
  description text,
  status text DEFAULT 'a_reparer'::text,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT tent_incidents_pkey PRIMARY KEY (id),
  CONSTRAINT tent_incidents_tent_id_fkey FOREIGN KEY (tent_id) REFERENCES public.tents(id)
);
CREATE TABLE public.camp_attendance (
  id integer NOT NULL DEFAULT nextval('camp_attendance_id_seq'::regclass),
  camp_id uuid,
  adherent_id text NOT NULL,
  CONSTRAINT camp_attendance_pkey PRIMARY KEY (id),
  CONSTRAINT camp_attendance_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.camps(id)
);
CREATE TABLE public.camp_locations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  address text,
  contact_info text,
  description text,
  is_shared boolean DEFAULT false,
  group_name text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  latitude numeric,
  longitude numeric,
  CONSTRAINT camp_locations_pkey PRIMARY KEY (id)
);