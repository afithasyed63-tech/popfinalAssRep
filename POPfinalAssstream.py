import streamlit as st
import pandas as pd
if 'page' not in st.session_state:
    st.session_state.page='home'
if 'movlist' not in st.session_state:
    st.session_state.movlist={'Harry Potter':{'rating':4.9,'genre':'Fantasy','view':6100},
    'Pirates of the Caribbean':{'rating':4.8,'genre':'Fantasy','view':4600},
    'Jurassic Park':{'rating':4.2, 'genre':'Adventure','view':3000},
    'Inception':{'rating': 4.7,'genre':'Sci-Fi','view':4000},
    'The Dark Knight':{'rating':4.9,'genre':'Action','view':4800},
    'Interstellar':{'rating':4.6,'genre':'Sci-Fi','view':3900},
    'The Lion King':{'rating':4.5,'genre':'Animation','view':4000},
    'Toy Story':{'rating':4.3,'genre':'Animation','view':3500},
    'The Godfather':{'rating':4.9,'genre':'Crime','view':6000},
    'Pulp Fiction':{'rating':4.4,'genre':'Crime','view':3000},
    'Avengers Endgame':{'rating':4.8,'genre':'Action','view':5000},
    'The Hobbit':{'rating':4.1,'genre':'Fantasy','view':2000}}

if 'usdata' not in st.session_state:
    st.session_state.usdata=[]
#showing the home screen
if st.session_state.page=='home':
    st.title("MOVIE APP")
    usname = st.text_input("enter your name : ")
    usid_no = st.text_input("enter your id number : ")
    uspassword = st.text_input("enter your password : ")
    sel_us = st.selectbox("select this",['user', 'admin'])
    if st.button('login'):
        if 'usname' not in st.session_state:
            st.session_state.name = usname
            st.session_state.usdata.append(usname)
        if 'usid_no' not in st.session_state:
            st.session_state.id_no = usid_no
        if 'uspassword' not in st.session_state:
            st.session_state.uspassword = uspassword
        if sel_us=='user':
            st.session_state.page='user page'
            st.rerun()
        else:
            st.session_state.page='admin page'
            st.rerun()

elif st.session_state.page=='user page':
    st.session_state.sel_op=st.selectbox("select the one you want to do",['select movie & rate','get recommandations','search the movie'])
    if st.session_state.sel_op=='select movie & rate':
        if 'views_mov' not in st.session_state:
            st.session_state.views_mov=[]
        if 'mov_rating' not in st.session_state:
            st.session_state.mov_rating={}
        if 'mov_rating1' not in st.session_state:
            st.session_state.mov_rating1=[]
        st.session_state.mov_name_sel=st.selectbox('Select Movie Name',list(st.session_state.movlist.keys()))
        st.session_state.rate_mov=st.slider('Select Movie Rating',0.0,5.0,1.0)
        if st.button('add rating'):
            st.session_state.views_mov.append(st.session_state.mov_name_sel)
            st.session_state.mov_rating[st.session_state.mov_name_sel]=st.session_state.rate_mov
            st.session_state.movlist[st.session_state.mov_name_sel]['view'] = st.session_state.movlist[st.session_state.mov_name_sel]['view'] + 1
            rate={'movie':st.session_state.mov_name_sel,
                  'rate':st.session_state.rate_mov,
                  'genre':st.session_state.movlist[st.session_state.mov_name_sel]['genre'],
                  'view':len(st.session_state.views_mov)}
            st.session_state.mov_rating1.append(rate)
            st.write('the rating is saved')
        if st.button('back to home'):
            st.session_state.page='home'
            st.rerun()

    elif st.session_state.sel_op=='get recommandations':
        def recom_gen():
            if len(st.session_state.views_mov) == 0:
                st.warning('you have no views')
                return
            # get last movie name
            last_mov = st.session_state.views_mov[-1]
            mov_gen = st.session_state.movlist[last_mov]['genre']
            for mov, rat in st.session_state.movlist.items():
                if rat['genre'] == mov_gen:
                    if mov != last_mov:
                        st.write(f"you watched this movie {last_mov} so we recommend this for you {mov}")

        def recom_rate():
            # get movie with greater rating
            for mov, rat in st.session_state.movlist.items():
                if rat['rating'] > 4.8:
                    st.write(
                        f"these movies are highly rated {mov} {rat['rating']} also this movie got {rat['view']} views")

        recom_gen()
        recom_rate()
        if st.button('back to home'):
            st.session_state.page = 'home'
            st.rerun()

    elif st.session_state.sel_op=='search the movie':
        nt=st.text_input('enter movie title or genre').lower()
        f=False
        for mov,rat in st.session_state.movlist.items():
            if nt in mov.lower() or nt in rat['genre'].lower():
                f=True
                st.write(f"'movie', {mov}, 'genre', {rat['genre']}, 'rating', {rat['rating']}, 'view',{rat['view']}")
        if not f:
            st.error('nothing found')
        if st.button('go to dashboard'):
            st.session_state.page='dashboard'
            st.rerun()
        if st.button('back to home'):
            st.session_state.page = 'home'
            st.rerun()

elif st.session_state.page=='dashboard':
    uspass=st.text_input('enter your password to protect your account')
    if uspass==st.session_state.uspassword:
        #give recommendations based on last watched movie
        st.subheader('recommendations')
        if len(st.session_state.views_mov)>0:
            last_mov = st.session_state.views_mov[-1]
            mov_gen = st.session_state.movlist[last_mov]['genre']
            for mov, rat in st.session_state.movlist.items():
                if rat['genre'] == mov_gen:
                    if mov != last_mov:
                        st.write(f"you watched this movie {last_mov} so we recommend this for you {mov}")
        else:
            st.error('you have no views')
        st.subheader('trending movies and top genre')
        # find the top6 movie
        tmovlist = st.session_state.movlist.copy()
        for i in range(6):
            hv = -1
            for hview in tmovlist:
                if tmovlist[hview]['view'] > hv:
                    hv = tmovlist[hview]['view']
                    t3 = hview
            st.write(f"the highest view trending in the movies is: {t3}")
            del tmovlist[t3]
        # find the top genre
        gen_tot = {}
        for mov in st.session_state.movlist:
            gentot = st.session_state.movlist[mov]['genre']
            if gentot in gen_tot:
                gen_tot[gentot] = gen_tot[gentot] + 1
            else:
                gen_tot[gentot] = 1
        hsco = 0
        for gentot in gen_tot:
            if gen_tot[gentot] > hsco:
                hsco = gen_tot[gentot]
                popgen = gentot
        st.write(f"the popular genre in the movies is: {popgen}")
        if st.session_state.mov_rating1:
            st.subheader('watch history and rating log')
            h1,h2,h3,h4=st.columns(4)
            h1.write('movie')
            h2.write('rating')
            h3.write('genre')
            h4.write('view')
            for e in st.session_state.mov_rating1:
                col1,col2,col3,col4=st.columns(4)
                col1.write(e['movie'])
                col2.write(e['rate'])
                col3.write(e['genre'])
                col4.write(e['view'])
        else:
            st.write('no rating log')
        #visualize bar chart for rating movies
        st.subheader('charts')
        tpmovs=[]
        tpnam=[]
        for mov,rat in st.session_state.movlist.items():
            tpnam.append(mov)
            tpmovs.append(rat['rating'])
        chd={'movie':tpnam,'rating':tpmovs}
        st.bar_chart(x='movie',y='rating',data=chd)
        if st.button('back to home'):
            st.session_state.page = 'home'
            st.rerun()

elif st.session_state.page=='admin':
    pas=st.text_input('enter your password to protect your account')
    if pas==st.session_state.uspassword:
        st.session_state.sel_ad_op=st.selectbox('select one operation',['add','edit','remove'])
        if st.session_state.sel_ad_op=='add':
            mov=st.text_input('enter the movie to add in the movie list')
            rat=st.text_input('enter the rating to add in the movie list')
            gen=st.text_input('enter the genre to add in the movie list')
            view=st.text_input('enter the view to add in the movie list')
            if st.button('add in the list'):
                st.session_state.movlist[mov]={'rating':float(rat),'genre':gen,'view':int(view)}
                st.write('added these in the movie list')
                st.write(st.session_state.movlist)
        elif st.session_state.sel_ad_op=='edit':
            mov=st.selectbox('enter the movie to edit the movie list',list(st.session_state.movlist.keys()))
            rat=st.text_input('enter the rating to add in the movie list')
            gen=st.text_input('enter the genre to add in the movie list')
            view=st.text_input('enter the view to add in the movie list')
            if st.button('edit the movie list'):
                st.session_state.movlist[mov]['rating']=float(rat)
                st.session_state.movlist[mov]['genre']=gen
                st.session_state.movlist[mov]['view']=int(view)
                st.write('edited these in the movie list')
                st.write(st.session_state.movlist)
        elif st.session_state.sel_ad_op=='remove':
            mov=st.selectbox('enter the movie to remove from the movie list',list(st.session_state.movlist.keys()))
            if st.button('remove the movie'):
                del st.session_state.movlist[mov]
                st.write('removed these in the movie list')
                st.write(st.session_state.movlist)

        if st.button('back to home'):
            st.session_state.page = 'home'
            st.rerun()

        st.subheader('most watched movie')
        # find the top6 movie
        tmovlist = st.session_state.movlist.copy()
        for i in range(6):
            hv = -1
            for hview in tmovlist:
                if tmovlist[hview]['view'] > hv:
                    hv = tmovlist[hview]['view']
                    t3 = hview
            st.write(f"the highest view trending in the movies is: {t3}")
            del tmovlist[t3]

        st.subheader('watch user')
        wcou=len(st.session_state.get('views_mov',[]))
        if wcou>8:
            stat='most watched user'
            st.write(stat)
        elif wcou>4:
            stat='medium watched user'
            st.write(stat)
        else:
            stat='low watched user'
            st.write(stat)

        st.subheader('trending movies based on ratings')
        tmovlist = st.session_state.movlist.copy()
        for i in range(6):
            hv = -1.0
            for hview in tmovlist:
                if tmovlist[hview]['rating'] > hv:
                    hv = tmovlist[hview]['rating']
                    t3 = hview
            st.write(f"the highest view trending in the movies is: {t3}")
            del tmovlist[t3]

        st.subheader('chart')
        tpmovs = []
        tpnam = []
        for mov, rat in st.session_state.movlist.items():
            tpnam.append(mov)
            tpmovs.append(rat['rating'])
        chd = {'movie': tpnam, 'rating': tpmovs}
        st.bar_chart(x='movie', y='rating', data=chd)

        tpmovs = []
        tpnam = []
        for mov, rat in st.session_state.movlist.items():
            tpnam.append(mov)
            tpmovs.append(rat['view'])
        chd = {'movie': tpnam, 'view': tpmovs}
        st.bar_chart(x='movie', y='view', data=chd)

        if st.button('back to home'):
            st.session_state.page = 'home'
            st.rerun()
    else:
        st.warning('wrong password')











