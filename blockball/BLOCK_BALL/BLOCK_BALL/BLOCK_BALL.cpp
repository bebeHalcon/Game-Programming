#include <windows.h>
#include <string>
#include <SDL.h>
#include <SDL_image.h>
#include <SDL_mixer.h>
#include <SDL_ttf.h>
#include <iostream>
#include <conio.h>
#include <fstream>
#include <ctime>
#undef main
using namespace std;

const int SCREEN_WIDTH = 1200;
const int SCREEN_HEIGHT = 600;
const int SCREEN_BPP = 32;
Mix_Chunk* sound[3];
Mix_Music* bkmusic, * loadmusic, * victorymusic, * creditmusic, * gameovermusic;
Mix_Music* stagemusic[8];

const int xdau = 200, xcuoi = 1000, ydau = 50, ycuoi = 550, MAXBLOCKx = 12, MAXBLOCKy = 8, MAXball = 5, xHPboss = 850, yHPboss = 0;
int somon = 0, sotele = 0, soball = 1, soitemdrop/*vat pham roi ra tu quai*/ = 0, heart = 5, stage = 0, t_clear = 0, socontinue = 0;;
long t_big, t_super;
/* item 0: phan than
   item 1: phong 
   item 2: di xuyen cac block thong thuong
*/   
bool get_item[3] = { false , false, false }; //kiem tra xem co an vat pham ko
bool multiplay = false, kt_conti = true, playextra = false;

SDL_Surface* g_screen = NULL;
SDL_Surface* g_bkground = NULL;
SDL_Surface* g_image = NULL;
SDL_Event g_even, g_trash; //su kien phim chinh cua game, su kien intro, su kien nhan phim thua
TTF_Font* font = TTF_OpenFont("D:/C++/BLOCK_BALL/FVF Fernando 08.ttf", 24);

// this is the color in rgb format,
// maxing out all would give you the color white,
// and it will be your text's color
SDL_Color White = { 255, 255, 255 };

// as TTF_RenderText_Solid could only be used on
// SDL_Surface then you have to create the surface first
//SDL_Surface* surfaceMessage = TTF_RenderText_Solid(font, "put your text here", White);


bool Init()
{
    if (SDL_Init(SDL_INIT_EVERYTHING) == -1)
    {
        return false;
    }
    TTF_Init();
    g_screen = SDL_SetVideoMode(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_BPP, SDL_SWSURFACE);
    if (g_screen == NULL)
        return false;
    if (Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 2, 4096) == -1) return false;
    /*music = Mix_LoadWAV("Bonus.wav");
    music0 = Mix_LoadWAV("true_arena.wav");*/
    sound[1] = Mix_LoadWAV("sound3.wav");
    sound[0] = Mix_LoadWAV("sound_victory.wav");
    sound[2] = Mix_LoadWAV("sound_bossdie.wav");

    bkmusic = Mix_LoadMUS("m_great_fairy.wav");
    loadmusic = Mix_LoadMUS("m_girls_are_resting.wav");
    victorymusic = Mix_LoadMUS("m_victory.wav");
    creditmusic = Mix_LoadMUS("m_settlement.wav");
    gameovermusic = Mix_LoadMUS("m_victory_imposter.wav");

    stagemusic[0] = Mix_LoadMUS("m_yogurt_yard.wav");
    stagemusic[1] = Mix_LoadMUS("m_snowdin.wav");
    stagemusic[2] = Mix_LoadMUS("m_rainbow_resort.wav");
    stagemusic[3] = Mix_LoadMUS("m_guard_room.wav");
    stagemusic[4] = Mix_LoadMUS("m_helper_to_hero.wav");
    stagemusic[5] = Mix_LoadMUS("m_true_arena.wav");
    stagemusic[6] = Mix_LoadMUS("m_uwasotemperate.wav");
    stagemusic[7] = Mix_LoadMUS("m_uwasoholiday.wav");

    return true;
}
SDL_Surface* LoadImage(std::string file_path)
{
    SDL_Surface* load_image = NULL;
    SDL_Surface* optimize_image = NULL;
    load_image = IMG_Load(file_path.c_str());
    if (load_image != NULL)
    {
        optimize_image = SDL_DisplayFormat(load_image);
        SDL_FreeSurface(load_image);
        if (optimize_image != NULL)
        {
            UINT32 color_key = SDL_MapRGB(optimize_image->format, 0, 0xFF, 0xFF);
            SDL_SetColorKey(optimize_image, SDL_SRCCOLORKEY, color_key);
        }
    }
    return optimize_image;
}
void ApplySurface(SDL_Surface* src, SDL_Surface* des, int x, int y)
{
    SDL_Rect offset;
    offset.x = x;
    offset.y = y;
    SDL_BlitSurface(src, NULL, des, &offset);
}
void CleanUp()
{
    SDL_FreeSurface(g_screen);
    //SDL_FreeSurface(g_bkground);
    SDL_FreeSurface(g_image);
}
void print_image(SDL_Surface*i1, SDL_Surface* i2, int x, int y)
{
    g_image = i1;
    ApplySurface(g_image, g_screen, x, y);
    CleanUp();
}
//---------------------------------------------------------------------------------------
bool inblock(float x, float y, int xhit, int yhit, int size, int dai, int rong)
{
    if ((int(x) + size >= xhit && int(x) <= xhit + dai) && (int(y) + size >= yhit && int(y) <= yhit + rong))
        return true;
    return false;
}

class thanh
{
public:
    int sized = 100, sizer = 10, speed = 2; //size theo chieu dai va rong, toc do di chuyen
    int xn=303, yd=300; // x cua thanh ngang, y cua thanh doc
    bool movex = false, movey = false; // kiem tra xem cac thanh co dang di chuyen hay ko
    long t_freezen = 0, t_freezed = 0, t_reverse = 0; //thoi gian bi bat dong cua thanh ngang/doc;
private:
    //SDLKey k;
    int dy = 0, dx = 0, dy2 = 0, dx2 = 0;
public:
    void edisplay()
    {
        if (sized == 60)
        {
            print_image(LoadImage("engangshort.png"), g_screen, xn, ydau);
            print_image(LoadImage("engangshort.png"), g_screen, xn, ycuoi);
            print_image(LoadImage("edocshort.png"), g_screen, xdau, yd);
            print_image(LoadImage("edocshort.png"), g_screen, xcuoi, yd);
        }
        else
        {
            print_image(LoadImage("ethanhngang.png"), g_screen, xn, ydau);
            print_image(LoadImage("ethanhngang.png"), g_screen, xn, ycuoi);
            print_image(LoadImage("ethanhdoc.png"), g_screen, xdau, yd);
            print_image(LoadImage("ethanhdoc.png"), g_screen, xcuoi, yd);
        }
    }
    void display()
    {
        if (sized == 60)
        {
            if (t_freezen != 0)
            {
                print_image(LoadImage("thanhngangshortf.png"), g_screen, xn, ydau);
                print_image(LoadImage("thanhngangshortf.png"), g_screen, xn, ycuoi);
            }
            else if (t_reverse == 0)
            {
                print_image(LoadImage("thanhngangshort.png"), g_screen, xn, ydau);
                print_image(LoadImage("thanhngangshort.png"), g_screen, xn, ycuoi);
            }

            if (t_freezed != 0)
            {
                print_image(LoadImage("thanhdocshortf.png"), g_screen, xdau, yd);
                print_image(LoadImage("thanhdocshortf.png"), g_screen, xcuoi, yd);
            }
            else if (t_reverse == 0)
            {
                print_image(LoadImage("thanhdocshort.png"), g_screen, xdau, yd);
                print_image(LoadImage("thanhdocshort.png"), g_screen, xcuoi, yd);
            }
        }
        else
        {
            if (t_freezen != 0)
            {
                print_image(LoadImage("thanhngangf.png"), g_screen, xn, ydau);
                print_image(LoadImage("thanhngangf.png"), g_screen, xn, ycuoi);
            }
            else if (t_reverse == 0)
            {
                print_image(LoadImage("thanhngang.png"), g_screen, xn, ydau);
                print_image(LoadImage("thanhngang.png"), g_screen, xn, ycuoi);
            }

            if (t_freezed != 0)
            {
                print_image(LoadImage("thanhdocf.png"), g_screen, xdau, yd);
                print_image(LoadImage("thanhdocf.png"), g_screen, xcuoi, yd);
            }
            else if (t_reverse == 0)
            {
                print_image(LoadImage("thanhdoc.png"), g_screen, xdau, yd);
                print_image(LoadImage("thanhdoc.png"), g_screen, xcuoi, yd);
            }

            if (t_reverse > 0)
            {
                print_image(LoadImage("thanhngangr.png"), g_screen, xn, ydau);
                print_image(LoadImage("thanhngangr.png"), g_screen, xn, ycuoi);
                print_image(LoadImage("thanhdocr.png"), g_screen, xdau, yd);
                print_image(LoadImage("thanhdocr.png"), g_screen, xcuoi, yd);
            }
        }
    }
    void move()
    {
        //cout << time(0) << " " << t_freezen << " " << t_freezed << endl;
        if (time(0) - t_freezen == 3) t_freezen = 0;
        if (time(0) - t_freezed == 3) t_freezed = 0;
        if (time(0) - t_reverse == 10) t_reverse = 0;

        movex = false; movey = false;
        if (g_even.type == SDL_KEYDOWN)
            switch (g_even.key.keysym.sym)
            {
            case SDLK_w: if (multiplay == false)
            {
                if (t_reverse > 0) dy = speed; else dy = -speed;
                dy2 = 0;
            }
                break;
            case SDLK_o: if (multiplay == true)
            {
                if (t_reverse > 0) dy = speed; else dy = -speed;
                dy2 = 0;
            }
                break;
            case SDLK_s: if (multiplay == false)
            {
                if (t_reverse > 0) dy2 = -speed; else dy2 = +speed;
                dy = 0;
            }
                break;
            case SDLK_l: if (multiplay == true)
            {
                if (t_reverse > 0) dy2 = -speed; else dy2 = +speed;
                dy = 0;
            }
                break;
            case SDLK_a: if (t_reverse > 0)dx = +speed; else dx = -speed; 
                dx2 = 0;
                break;
            case SDLK_d: if (t_reverse > 0) dx2 = -speed; else dx2 = +speed; 
                dx = 0;
                break;
            }
        if (g_even.type == SDL_KEYUP)
            switch (g_even.key.keysym.sym)
            {
            case SDLK_w: dy = 0;
                break;
            case SDLK_o: dy = 0;
                break;
            case SDLK_s: dy2 = 0;
                break;
            case SDLK_l: dy2 = 0;
                break;
            case SDLK_a: dx = 0;
                break;
            case SDLK_d: dx2 = 0;
                break;
            }
        if (t_freezen != 0) dx = dx2 = 0;
        if (t_freezed != 0) dy = dy2 = 0;

        if (dx + dx2 != 0) movex = true;
        if (dy + dy2 != 0) movey = true;

        xn += dx + dx2;
        yd += dy + dy2;

        if (xn < xdau) { xn += speed; movex = false; }
        if (xn > xcuoi - sized + 10) { xn -= speed; movex = false; }
        if (yd < ydau) { yd += speed; movey = false; }
        if (yd > ycuoi - sized + 10) { yd -= speed; movey = false; }
    }
};
thanh th;

class block
{
public:
    int x = 0, y = 0;
    int sized = 100, sizer = 20;
    int no = 0, t = 0;//ma so cua block va bien thoi gian hieu ung anh dong
    int no0 = no; //luu ma so ban dau cua block
    bool broke_effect = false;
public:
    void broke()
    {
        t++;
        if (no0 >= 1 && no0 <= 3)
        {
            if (t == 1) print_image(LoadImage("broke1.png"), g_screen, x, y);
            if (t == 10) print_image(LoadImage("broke2.png"), g_screen, x, y);
            if (t == 20) print_image(LoadImage("broke3.png"), g_screen, x, y);
            if (t == 30) print_image(LoadImage("broke4.png"), g_screen, x, y);
            if (t == 40) print_image(LoadImage("broke5.png"), g_screen, x, y);
            if (t == 50) { print_image(LoadImage("eblock.png"), g_screen, x, y); t = 0; broke_effect = false; }
        }
        if (no0 >= 4 && no0 <= 7)
        {
            if (t == 1) print_image(LoadImage("brokev1.png"), g_screen, x, y);
            if (t == 10) print_image(LoadImage("brokev2.png"), g_screen, x, y);
            if (t == 20) print_image(LoadImage("brokev3.png"), g_screen, x, y);
            if (t == 30) print_image(LoadImage("brokev4.png"), g_screen, x, y);
            if (t == 40) print_image(LoadImage("brokev5.png"), g_screen, x, y);
            if (t == 50) { print_image(LoadImage("eblockv.png"), g_screen, x, y); t = 0; broke_effect = false; }
        }

    }
    void edisplay()
    {
        if (no0 < 0) { print_image(LoadImage("eitem.png"), g_screen, x, y); }
        else print_image(LoadImage("eblock.png"), g_screen, x, y);
    }
    void display()
    {
        if (no == 1) print_image(LoadImage("block1.png"), g_screen, x, y);
        if (no == 2) print_image(LoadImage("block2.png"), g_screen, x, y);
        if (no == 3) print_image(LoadImage("block3.png"), g_screen, x, y);
        if (no == 4 || no == 5) print_image(LoadImage("hardblock.png"), g_screen, x, y);
        if (no == 6) print_image(LoadImage("blockv1.png"), g_screen, x, y);
        if (no == 7) print_image(LoadImage("blockv2.png"), g_screen, x, y);
        if (no == -1) print_image(LoadImage("item.png"), g_screen, x, y);
        if (no == -2) print_image(LoadImage("item1.png"), g_screen, x, y);
        if (no == -3) print_image(LoadImage("item2.png"), g_screen, x, y);
        if (no == -4) print_image(LoadImage("heart.png"), g_screen, x, y);
    }
};
block blo[MAXBLOCKx][MAXBLOCKy];

class teleblock
{
public:
    int x = 0, y = 0, sized = 100, sizer = 20;
public:
    void display(int i)
    {
        if (i % 2 == 0) print_image(LoadImage("teleup.png"), g_screen, x, y);
        if (i % 2 == 1) print_image(LoadImage("teledown.png"), g_screen, x, y);
    }
};
teleblock tele[4];

class bullet
{
public:
    int x=0, y=0, size = 10;// no = 1;
    float xf=0, yf=0, alpha=0, dt = 1;
private:
    int t = 0;
public:
    void edisplay()
    {
        print_image(LoadImage("eball.png"), g_screen, x, y);
    }
    void display()
    {
        t++;
        if (t < 30) print_image(LoadImage("bullet.png"), g_screen, x, y);
        else if (t < 60) print_image(LoadImage("bullet2.png"), g_screen, x, y);
        else t = 0;
    }
    void move()
    {
        yf += -sin(alpha / 180.0 * 3.14) * dt;
        xf += cos(alpha / 180.0 * 3.14) * dt;
        x = int(xf);
        y = int(yf);
        //cout << "   X = " << x << "   Y= " << y;
    }
};
bullet bu[8];

void delete_bullet(int k) //xoa bu[k] (bullet thu [k])
{
    bu[k].edisplay();
    bu[k].x = 0; bu[k].y = 0; bu[k].xf = 0; bu[k].yf = 0;
}

class monster
{
public:
    int x = 0, y = 0;
    float speed = 0.5, xf = 0, yf = 0, x0 = 0, y0 = 0, xball, yball /*toa do cua ball*/;
    int sized = 40, sizer = 30;
    int no = 0; //ma so cua monster
    int dichuyen = 0, HP = 2;
    bool hit_effect = false, atk_effect = false; //hieu ung khi bi ball cham trung
private:
    int t = 0, t_hit = 0, t_atk = 0; //cac bien thoi gian hieu ung anh dong
    int ran = 0;
    float xc, yc; //toa do cuoi di chuyen
    float sdx[4], sdy[4];
public:
    void start(int i, int j, int di)
    {
        xf = i; x0 = i;
        yf = j; y0 = j;
        dichuyen = di;
        if (no >= 1 && no <= 4)
        {
            xc = x0 - 2 * (x0 - (xcuoi + xdau) / 2) -40;
            yc = y0 - 2 * (y0 - (ycuoi + ydau) / 2) -44;
        }
    }
    void edisplay()
    {
        if (!(x == 0 && y == 0))
        {
            if (no == 5) print_image(LoadImage("eblockv.png"), g_screen, x, y);
            else if (no == 8 || no == 9) print_image(LoadImage("etruekaslime.png"), g_screen, x, y);
            else if (no == 10) print_image(LoadImage("eghost.png"), g_screen, x, y);
            else print_image(LoadImage("emon.png"), g_screen, x, y);
        }
    }
    void transform()
    {
        Mix_HaltMusic();
        SDL_Delay(500);
        y0 = float(y); x0 = float(x); yc = 250; xc = 550;
        while (!(x == 550 && y == 250))
        {
            print_image(LoadImage("ekaslime.png"), g_screen, x, y);
            yf += -((y0 - yc) / sqrt((y0 - yc) * (y0 - yc) + (x0 - xc) * (x0 - xc))) * speed;
            xf += ((xc - x0) / sqrt((y0 - yc) * (y0 - yc) + (x0 - xc) * (x0 - xc))) * speed;
            x = int(xf); y = int(yf);
            print_image(LoadImage("kaslime_hit.png"), g_screen, x, y);
            SDL_Delay(1);
            SDL_Flip(g_screen);
        }

        Mix_PlayMusic(stagemusic[5], -1);
        for (int i = 0; i < 10; i++)
        {
            if (i % 2 == 0)
            {
                print_image(LoadImage("etruekaslime.png"), g_screen, x, y);
                print_image(LoadImage("kaslimedown1.png"), g_screen, x, y);
            }
            else print_image(LoadImage("truetransform1.png"), g_screen, x, y);
            SDL_Delay(100);
            SDL_Flip(g_screen);
        }
        for (int i = 0; i < 10; i++)
        {
            if (i % 2 == 0) print_image(LoadImage("truetransform1.png"), g_screen, x, y);
            else print_image(LoadImage("truetransform2.png"), g_screen, x, y);
            SDL_Delay(100);
            SDL_Flip(g_screen);
        }
        for (int i = 0; i < 10; i++)
        {
            if (i % 2 == 0) print_image(LoadImage("truetransform2.png"), g_screen, x, y);
            else print_image(LoadImage("truekaslime1.png"), g_screen, x, y);
            SDL_Delay(100);
            SDL_Flip(g_screen);
        }
        SDL_Delay(1000);
        for (int i = 0; i < 35; i++)
        {
            if (i == 28) print_image(LoadImage("smoke1.png"), g_screen, 0, 0);
            if (i == 29) print_image(LoadImage("smoke2.png"), g_screen, 0, 0);
            if (i == 30)
            {
                print_image(LoadImage("bkground.png"), g_screen, 0, 0);
                print_image(LoadImage("smoke3.png"), g_screen, 0, 0);
            }
            if (i == 31)
            {
                print_image(LoadImage("bkground.png"), g_screen, 0, 0);
                print_image(LoadImage("smoke4.png"), g_screen, 0, 0);
            }
            if (i == 32)
            {
                print_image(LoadImage("bkground.png"), g_screen, 0, 0);
                print_image(LoadImage("smoke5.png"), g_screen, 0, 0);
            }
            if (i == 33)
            {
                print_image(LoadImage("bkground.png"), g_screen, 0, 0);
                print_image(LoadImage("smoke6.png"), g_screen, 0, 0);
            }
            if (i % 2 == 0) print_image(LoadImage("truegrowl1.png"), g_screen, x, y);
            else print_image(LoadImage("truegrowl2.png"), g_screen, x, y);
            SDL_Delay(75);
            SDL_Flip(g_screen);
        }
        print_image(LoadImage("bkground.png"), g_screen, 0, 0);
        print_image(LoadImage("HPboss.png"), g_screen, xHPboss, yHPboss);
        for (int i = 1; i <= heart; i++) print_image(LoadImage("heart.png"), g_screen, i * 20, 10); //in so heart
        no = 8;
        sized = 100; sizer = 80;
        speed = 1.5; dichuyen = 1;
        x0 = xf; y0 = yf; xc = xf; yc = yf;
        sdx[1] = sdx[2] = sdx[3] = xf; 
        sdy[1] = sdy[2] = sdy[3] = yf;
        th.sized = 60; th.t_reverse = 0;
    }
    void hiteffect()
    {
        if (no >= 6) print_image(LoadImage("eitem.png"), g_screen, xHPboss + 80 + (HP - 1) % 10 * 20, 2);
        t_hit++;
        if (no >= 1 && no <= 3)
        {
            if (t_hit < 30) print_image(LoadImage("slime_hit2.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("slime_hit.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("slime_hit2.png"), g_screen, x, y);
            else print_image(LoadImage("slime_hit.png"), g_screen, x, y);
        }
        if (no == 4)
        {
            if (t_hit < 30) print_image(LoadImage("slime_hit2.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("slime2_hit.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("slime_hit2.png"), g_screen, x, y);
            else print_image(LoadImage("slime2_hit.png"), g_screen, x, y);
        }
        if (no == 5)
        {
            if (t_hit < 30) print_image(LoadImage("aneye_hit2.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("aneye_hit.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("aneye_hit2.png"), g_screen, x, y);
            else print_image(LoadImage("aneye_hit.png"), g_screen, x, y);
        }
        if (no == 6 || no == 7)
        {
            if (t_hit < 30) print_image(LoadImage("kaslime_hit2.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("kaslime_hit.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("kaslime_hit2.png"), g_screen, x, y);
            else print_image(LoadImage("kaslime_hit.png"), g_screen, x, y);
        }
        //t_hit = 300;
        if (t_hit >= 300) 
        { 
            //if (no == 7) print_image(LoadImage("ekaslime.png"), g_screen, x, y);
            hit_effect = false; t_hit = 0;
            if (get_item[1] == true) HP -= 2;
            else HP--;
            if (HP <= 0)
            {
                if (no >= 6) Mix_PlayChannel(-1, sound[2], 0);
                HP = 0;
                edisplay();
                srand(time(0)); //random item roi ra

                int ra = rand() % 12;
                cout << ra <<" "<<rand()<<" "<<rand()<< endl;
                if (ra <= 6 && soitemdrop < MAXBLOCKx)
                {
                    //cout << ra << " " << soitemdrop << endl;
                    if (ra >= 0 && ra<= 1) blo[soitemdrop][MAXBLOCKy-1].no = -1;
                    if (ra >= 2 && ra<= 3) blo[soitemdrop][MAXBLOCKy-1].no = -2;
                    if (ra >= 4 && ra<= 5) blo[soitemdrop][MAXBLOCKy-1].no = -3;
                    if (ra == 6) blo[soitemdrop][MAXBLOCKy-1].no = -4;
                    blo[soitemdrop][MAXBLOCKy - 1].x = x + sized / 2 - 10;
                    blo[soitemdrop][MAXBLOCKy - 1].y = y + sizer / 2 - 10;
                    blo[soitemdrop][MAXBLOCKy - 1].sizer = blo[soitemdrop][MAXBLOCKy - 1].sized = 20;
                    blo[soitemdrop][MAXBLOCKy - 1].display();
                    soitemdrop++;
                }
            }
            if (no == 7 && HP == 10) transform();
            if (no == 10)
            {
                if (HP > 0)
                {
                    srand(time(0));
                    edisplay();
                    if (!(sdx[1] == 0 && sdy[1] == 0))
                    {
                        print_image(LoadImage("eghost.png"), g_screen, sdx[1], sdy[1]);
                        print_image(LoadImage("eghost.png"), g_screen, sdx[2], sdy[2]);
                    }
                    do
                    {
                        xf = float(xdau + 30 + rand() % (xcuoi - sized - 30 - (xdau + 30) + 1));
                        yf = float(ydau + 30 + rand() % (ycuoi - sizer - 30 - (ydau + 30) + 1));
                        sdx[1] = float(xdau + 30 + rand() % (xcuoi - sized - 30 - (xdau + 30) + 1));
                        sdy[1] = float(ydau + 30 + rand() % (ycuoi - sizer - 30 - (ydau + 30) + 1));
                        sdx[2] = float(xdau + 30 + rand() % (xcuoi - sized - 30 - (xdau + 30) + 1));
                        sdy[2] = float(ydau + 30 + rand() % (ycuoi - sizer - 30 - (ydau + 30) + 1));
                        x = int(xf); y = int(yf);
                        x0 = xf; y0 = yf;
                    } while (inblock(xball, yball, x, y, 10, sized, sizer) == true);
                }
                else
                {
                    Mix_HaltMusic();
                    SDL_Delay(1000);
                    Mix_PlayMusic(stagemusic[7], 0);
                    edisplay();
                    if (!(sdx[1] == 0 && sdy[1] == 0))
                    {
                        print_image(LoadImage("eghost.png"), g_screen, sdx[1], sdy[1]);
                        print_image(LoadImage("eghost.png"), g_screen, sdx[2], sdy[2]);
                    }
                    SDL_Flip(g_screen);
                    x = 550; y = 250;
                    print_image(LoadImage("ghostthank.png"), g_screen, x, y);
                    SDL_Flip(g_screen);
                    SDL_Delay(1000);

                    while (y >= (0 - sizer - 10))
                    {
                        //cout << x << "   " << y << endl;
                        print_image(LoadImage("ghostthank.png"), g_screen, x, y);
                        ran++;
                        if (ran > 10000) ran = 0;
                        x = int(x0 + 5 * sin(0.1 * ran));
                        y--;
                        SDL_Delay(75);
                        SDL_Flip(g_screen);
                    }
                    t_clear = 200;
                }
            }
        }
        if (no == 8)
        {
            if (t_hit < 30) print_image(LoadImage("truekaslime_hit2.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("truekaslime_hit.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("truekaslime_hit2.png"), g_screen, x, y);
            else print_image(LoadImage("truekaslime_hit.png"), g_screen, x, y);
        }
        if (no == 9)
        {
            if (t_hit < 30) print_image(LoadImage("biganeye_hit2.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("biganeye_hit.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("biganeye_hit2.png"), g_screen, x, y);
            else print_image(LoadImage("biganeye_hit.png"), g_screen, x, y);
        }
        if (no == 10)
        {
            if (t_hit < 30) print_image(LoadImage("ghost_hit.png"), g_screen, x, y);
            else if (t_hit < 60) print_image(LoadImage("ghost.png"), g_screen, x, y);
            else if (t_hit < 90) print_image(LoadImage("ghost_hit.png"), g_screen, x, y);
            else print_image(LoadImage("ghost.png"), g_screen, x, y);
        }
    }
    void atkeffect()
    {
        t_atk++;
        if (no == 7)
        {
            if (t_atk < 30) print_image(LoadImage("kaslimedown2.png"), g_screen, x, y);
            else if (t_atk < 60) print_image(LoadImage("kaslimedown1.png"), g_screen, x, y);
            else if (t_atk < 120) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 150) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 180) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 210) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 240) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 270) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 300) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 330) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 360) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 390) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 420) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 450) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 480) print_image(LoadImage("kaslimecall1.png"), g_screen, x, y);
            else if (t_atk < 510) print_image(LoadImage("kaslimecall2.png"), g_screen, x, y);
            else if (t_atk < 540) print_image(LoadImage("kaslimedown1.png"), g_screen, x, y);
            else { print_image(LoadImage("kaslimedown2.png"), g_screen, x, y); th.t_reverse = time(0); }
        }
        if (t_atk >= 700 && (no == 8 || no == 7))
        {
            if (ran == 1) ran = 0;
            else ran = 1; //doi kieu tan cong
            t_atk = 0; atk_effect = false;
        }
        if (no == 8)
        {
            if (t_atk % 30 < 15) print_image(LoadImage("trueatk1.png"), g_screen, x, y);
            else print_image(LoadImage("trueatk2.png"), g_screen, x, y);

            if (ran == 1) //kieu tan cong 1:
                if (t_atk == 480)
                {
                    for (int i = 0; i < 8; i++)
                    {
                        delete_bullet(i);
                        bu[i].xf = x + sized / 2;
                        bu[i].yf = y + 10;
                        bu[i].x = int(bu[i].xf); bu[i].y = int(bu[i].yf);
                        bu[i].alpha = i * 45;
                        //cout << bu[i].x << "   " << bu[i].y << endl; _getch();
                    }
                }
            if (ran == 0) //tan cong kieu 2:
            {
                if (t_atk == 450 || t_atk == 500 || t_atk == 550 || t_atk == 600 || t_atk == 650)
                {
                    int i = (650 - t_atk) / 50;
                    bu[i].xf = x + sized / 2;
                    bu[i].yf = y + 10;
                    bu[i].x = int(bu[i].xf); bu[i].y = int(bu[i].yf);
                    bu[i].alpha = acos((xball-bu[i].xf) / sqrt(pow(xball - bu[i].xf, 2) + pow(bu[i].yf - yball, 2))) * 180 / 3.14;
                    if (yball > bu[i].yf) bu[i].alpha = 360 - bu[i].alpha;
                    bu[i].alpha = float(int(bu[i].alpha + 360) % 360);
                    //cout << bu[i].alpha <<" "<< bu[i].yf<<":"<<bu[i].xf<<":"<<xball<<":"<<yball<<endl;
                }
            }
        }
    }
    void display()
    {
        t++;
        if (no == 1 || no == 3)
        {
            if (t < 30) print_image(LoadImage("slime_11.png"), g_screen, x, y);
            else if (t < 60) print_image(LoadImage("slime_12.png"), g_screen, x, y);
            else t = 0;
        }
        if (no == 2)
        {
            if (t < 100) print_image(LoadImage("slime_21.png"), g_screen, x, y);
            else if (t < 200) print_image(LoadImage("slime_22.png"), g_screen, x, y);
            else t = 0;
        }
        if (no == 4)
        {
            if (t < 30) print_image(LoadImage("slime2_1.png"), g_screen, x, y);
            else if (t < 60) print_image(LoadImage("slime2_2.png"), g_screen, x, y);
            else t = 0;
        }
        if (no == 5)
        {
            if (t < 1200) print_image(LoadImage("aneye1.png"), g_screen, x, y);
            else if (t < 1233) print_image(LoadImage("aneye2.png"), g_screen, x, y);
            else if (t < 1267) print_image(LoadImage("aneye3.png"), g_screen, x, y);
            else if (t < 1300) print_image(LoadImage("aneye2.png"), g_screen, x, y);
            else t = 0;
        }
        if (no == 6)
        {
            if (t < 100) print_image(LoadImage("kaslime_sleep1.png"), g_screen, x, y);
            else if (t < 200) print_image(LoadImage("kaslime_sleep2.png"), g_screen, x, y);
            else t = 0;
        }
        if (no == 7)
        {
            if (dichuyen == 0)
            {
                if (t < 30) print_image(LoadImage("kaslimeright1.png"), g_screen, x, y);
                else if (t < 60) print_image(LoadImage("kaslimeright2.png"), g_screen, x, y);
                else t = 0;
            }
            if (dichuyen == 1)
            {
                if (t < 30) print_image(LoadImage("kaslimedown1.png"), g_screen, x, y);
                else if (t < 60) print_image(LoadImage("kaslimedown2.png"), g_screen, x, y);
                else t = 0;
            }
            if (dichuyen == 2)
            {
                if (t < 30) print_image(LoadImage("kaslimeleft1.png"), g_screen, x, y);
                else if (t < 60) print_image(LoadImage("kaslimeleft2.png"), g_screen, x, y);
                else t = 0;
            }
            if (dichuyen == 3)
            {
                if (t < 30) print_image(LoadImage("kaslimeup1.png"), g_screen, x, y);
                else if (t < 60) print_image(LoadImage("kaslimeup2.png"), g_screen, x, y);
                else t = 0;
            }
        }
        if (no == 8)
        {
            sdx[0] = x; sdy[0] = y; 
            
            if (t < 30) print_image(LoadImage("truekaslime1.png"), g_screen, sdx[0], sdy[0]);
            else if (t < 60) print_image(LoadImage("truekaslime2.png"), g_screen, sdx[0], sdy[0]);
            else t = 0;
        }
        if (no == 9)
        {
            if (yball >= y - 100 && yball <= y + 180 && xball >= 300 && xball <= 900)
            {
                if (yball >= y - 70 && yball <= y + 150)
                {
                    if (xball > 400 && xball <= x) print_image(LoadImage("biganeyeleft.png"), g_screen, x, y);
                    else if (xball > x && xball <= x + sized) print_image(LoadImage("biganeyeup.png"), g_screen, x, y);
                    else if (xball > x + sized && xball <= 800) print_image(LoadImage("biganeyeright.png"), g_screen, x, y);
                }
                else print_image(LoadImage("biganeye0.png"), g_screen, x, y);
            }
            else
            {
                if (t < 30) print_image(LoadImage("biganeye1.png"), g_screen, x, y);
                else if (t < 60) print_image(LoadImage("biganeye2.png"), g_screen, x, y);
                else if (t < 90) print_image(LoadImage("biganeye3.png"), g_screen, x, y);
                else if (t < 120) print_image(LoadImage("biganeye2.png"), g_screen, x, y);
                else t = 0;
            }
        }
        if (no == 10)
        {
            print_image(LoadImage("ghost.png"), g_screen, x, y);
            if (HP < 10)
            {
                print_image(LoadImage("ghost_hit.png"), g_screen, sdx[1], sdy[1]);
                print_image(LoadImage("ghost_hit.png"), g_screen, sdx[2], sdy[2]);
            }
        }
        //if (t >= 900) t = 0;
    }
    void move()
    {
        for (int i = 0; i < MAXBLOCKx; i++) //in lai item neu co quai vat di qua
            if (inblock(float(blo[i][MAXBLOCKy - 1].x), float(blo[i][MAXBLOCKy - 1].y), x, y, 20, sized, sizer)) blo[i][MAXBLOCKy - 1].display();
        if (no == 1 || no == 3 || no == 4)
        {
            if (dichuyen == 0) xf += speed;
            if (dichuyen == 1) yf += speed;
            if (dichuyen == 2) xf -= speed;
            if (dichuyen == 3) yf -= speed;
            //if (no == 1) { cout << x << " " << y << " " << xc << " " << yc << endl; _getch(); }
            if ((xf == x0 && yf == y0) || (xf == xc && yf == y0) 
                || (xf == xc && yf == yc) || (xf == x0 && yf == yc))
                if (no == 1 || no == 4)dichuyen++;
                else if (no == 3) dichuyen--;
            if (dichuyen > 3 && (no == 1 || no == 4)) dichuyen = 0;
            if (dichuyen < 0 && no == 3) dichuyen = 3;
        }
        if (no == 7)
        {
            if (int(xf) == x0 && int(yf) == y0)
            {
                print_image(LoadImage("ekaslime.png"), g_screen, x, y);
                srand(time(NULL)); dichuyen = rand() % 4;
            }
            if (int(xf) <= x0 - 300 || int(xf) >= x0 + 300 || int(yf) <= y0 - 150 || int(yf) >= y0 + 150)
            {
                print_image(LoadImage("ekaslime.png"), g_screen, x, y);
                dichuyen = (dichuyen + 2) % 4;
            }

            if (dichuyen == 0) xf += speed;
            if (dichuyen == 1) yf += speed;
            if (dichuyen == 2) xf -= speed;
            if (dichuyen == 3) yf -= speed;

            if (time(0) % 30 == 0) atk_effect = true;
        }
        if (no == 8)
        {
            if (time(0) % 3 == 0 && dichuyen != 0)
            {
                x0 = xf; y0 = yf;
                srand(time(NULL));
                xc = float(xdau+30 + rand() % (xcuoi - sized - 30 - (xdau+30) + 1));
                yc = float(ydau + 30 + rand() % (ycuoi - sizer - 30 - (ydau + 30) + 1));
                /*if (((xc - x0) * (xc - x0) + (yc - y0) * (yc - y0)) < 10000)
                {
                    xc = float((xcuoi - sized - xdau) / 2);
                    yc = float((ycuoi - sizer - ydau) / 2);
                }*/
                dichuyen = 0;
            }
            if (time(0) % 3 == 1) dichuyen = 1;
            if (abs(xf - xc) > 2 && abs(yf - yc) > 2)
            {
                edisplay();
                if (t % 20 == 0) for (int i = 3; i >= 1; i--)
                {
                    sdx[i] = sdx[i - 1];
                    sdy[i] = sdy[i - 1];
                }

                print_image(LoadImage("etruekaslime.png"), g_screen, sdx[3], sdy[3]);
                print_image(LoadImage("truekaslimesd2.png"), g_screen, sdx[2], sdy[2]);
                print_image(LoadImage("truekaslimesd1.png"), g_screen, sdx[1], sdy[1]);
                yf += -((y0 - yc) / sqrt((y0 - yc) * (y0 - yc) + (x0 - xc) * (x0 - xc))) * speed;
                xf += ((xc - x0) / sqrt((y0 - yc) * (y0 - yc) + (x0 - xc) * (x0 - xc))) * speed;
            }
            else if (sdx[2] != sdx[0] && sdy[2] != sdy[0])
            {
                print_image(LoadImage("etruekaslime.png"), g_screen, sdx[2], sdy[2]);
                print_image(LoadImage("etruekaslime.png"), g_screen, sdx[1], sdy[1]);
                sdx[2] = sdx[1] = sdx[0]; sdy[2] = sdy[1] = sdy[0];
            }

            if (time(0) % 30 == 0) { atk_effect = true;}
        }
        if (no == 10)
        {
            ran++;
            if (ran > 10000) ran = 0;
            xf = x0 + 5 * sin(0.04 * ran);
            yf = y0 - 5 * cos(0.04 * ran);
            //cout << xf << " " << yf <<"  "<<sin(1*ran)<<"  "<<ran<< endl;
        }
        x = int(xf); y = int(yf);
        if (no == 5 || no == 9)
        {
            bool kt = true;
            if (((time(0) % 15 == 0) || (time(0) % 15 == 7)) && kt == true)
            {
                kt = false;
                for (int i = 0; i < 4; i++)
                {
                    delete_bullet(i);
                    bu[i].xf = x + sized / 2;
                    bu[i].yf = y + sizer / 2;
                    bu[i].x = int(bu[i].xf); bu[i].y = int(bu[i].yf);
                    if (time(0) % 15 == 0) bu[i].alpha = i * 90;
                    if (time(0) % 15 == 7) bu[i].alpha = i * 90 + 45;
                    //cout << bu[i].x << "   " << bu[i].y << endl; _getch();
                }
            }
            if (time(0) % 15 != 0 && time(0) % 15 != 7) kt = true;
        }
    }
};
monster mon[10];

bool hitngang(float alpha, float x, float y, int xhit, int yhit, int size, int dai, int rong)
//toa do ball, toa do block, size ball (size), size block (dai,rong)
{
    if (int(y) >= yhit + rong - 5 && int(y) <= yhit + rong && int(x) + size >= xhit && int(x) <= xhit + dai)
    {
        if (alpha >= 180 || alpha == 0) return false;
        return true;
    }
    if (int(y) + size >= yhit && int(y) + size <= yhit + 5 && int(x) + size >= xhit && int(x) <= xhit + dai)
    {
        //return true;
        if (0 <= alpha && alpha <= 180) return false;
        return true;
    }
    return false;
}
bool hitdoc(float x, float y, int xhit, int yhit, int size, int dai, int rong)
//same
{
    if (((int(x) >= xhit + dai - 5 && int(x) <= xhit + dai) || (int(x) + size >= xhit && int(x) + size <= xhit + 5))
        && int(y) + size >= yhit && int(y) <= yhit + rong) return true;
    return false;
}

class ball
{
public: 
    float x = 0, y = 0, dt = 1;
    int alpha = 40, size = 10;
    float sdx[5], sdy[5];
private:
    int alpha0 = 45; //luu bien alpha
    int k = 0;
    bool chamx = false, chamy = false; //kiem tra xem bong co cham vao thanh ngang hoac doc ko (chamx: cham thanh ngang)
public:
    void edisplay()
    {
        if (get_item[1] == true)print_image(LoadImage("ebigball.png"), g_screen, x, y);
        else print_image(LoadImage("eball.png"), g_screen, x, y);
    }
    void eedisplay() //xoa sau khi ball ra ngoai
    {
        for (int i = 0; i < 5; i++) print_image(LoadImage("ebigball.png"), g_screen, sdx[i], sdy[i]);
    }
    void display()
    {
        if (mon[0].no == 8 || mon[0].no == 9) { dt = 1.2; mon[0].xball = x; mon[0].yball = y; }
        if (mon[0].no == 10) { dt = 1 + ((10 - mon[0].HP) * 0.15); }

        k++;
        if (k >= 100) k = 0;
        sdx[0] = x; sdy[0] = y;
        if (k % 10 == 0) for (int i = 4; i >= 1; i--)
        {
            sdx[i] = sdx[i - 1];
            sdy[i] = sdy[i - 1];
        }    

        if (get_item[1] == true)
        {
            print_image(LoadImage("ebigball.png"), g_screen, sdx[4], sdy[4]);
            print_image(LoadImage("bigball3.png"), g_screen, sdx[3], sdy[3]);
            print_image(LoadImage("bigball2.png"), g_screen, sdx[2], sdy[2]);
            print_image(LoadImage("bigball1.png"), g_screen, sdx[1], sdy[1]);
            print_image(LoadImage("bigball.png"), g_screen, sdx[0], sdy[0]);
        }
        else if (get_item[2] == true)
        {
            //cout << "AA";
            print_image(LoadImage("eball.png"), g_screen, sdx[4], sdy[4]);
            print_image(LoadImage("ball3.png"), g_screen, sdx[3], sdy[3]);
            print_image(LoadImage("superballsd2.png"), g_screen, sdx[2], sdy[2]);
            print_image(LoadImage("superballsd1.png"), g_screen, sdx[1], sdy[1]);
            if (k < 25) print_image(LoadImage("superball1.png"), g_screen, sdx[0], sdy[0]);
            else if (k < 50) print_image(LoadImage("superball2.png"), g_screen, sdx[0], sdy[0]);
            else if (k < 75) print_image(LoadImage("superball3.png"), g_screen, sdx[0], sdy[0]);
            else if (k < 100) print_image(LoadImage("superball4.png"), g_screen, sdx[0], sdy[0]);
        }
        else
        {
            print_image(LoadImage("eball.png"), g_screen, sdx[4], sdy[4]);
            print_image(LoadImage("ball3.png"), g_screen, sdx[3], sdy[3]);
            print_image(LoadImage("ball2.png"), g_screen, sdx[2], sdy[2]);
            print_image(LoadImage("ball1.png"), g_screen, sdx[1], sdy[1]);
            print_image(LoadImage("ball.png"), g_screen, sdx[0], sdy[0]);
        }
    }
    void display(bool i)//ham chi in ra cai bong cua ball luc ban dau chua ban ra hoi thanh
    {
        print_image(LoadImage("ball3.png"), g_screen, x, y);
    }
    void broke()
    {
        eedisplay();
        th.display();
        for (int i = 0; i < 4; i++)
        {
            //SDL_Flip(g_screen);
            Beep(659, 50);
            Beep(659, 50);
            if (i % 2 == 0) print_image(LoadImage("ball2.png"), g_screen, x, y);
            else print_image(LoadImage("ball.png"), g_screen, x, y);
            SDL_Delay(300);
            SDL_Flip(g_screen);
        }
        Mix_PlayChannel(-1, sound[1], 0);
        SDL_Delay(500);
        print_image(LoadImage("ballbroke.png"), g_screen, x, y);
        SDL_Flip(g_screen);
        SDL_Delay(2000);
        get_item[1] = false; edisplay();
        SDL_Flip(g_screen);
    }
    void move()
    {
        alpha0 = alpha;
        //xet cham voi cac thanh chan
        chamx = false; chamy = false;
        //if (x >= xdau-9 + th.sizer && x + size <= xcuoi+9 && y >= ydau-9 + th.sizer && y + size <= ycuoi+9)
        {
            //cout << alpha << " "<<hitngang(alpha, x, y, th.xn + 15, ycuoi, size, th.sized - 30, th.sizer) << endl;
            //_getch();
            if (hitngang(alpha, x, y, th.xn + 15, ydau, size, th.sized - 30, th.sizer) 
                || hitngang(alpha, x, y, th.xn + 15, ycuoi, size, th.sized - 30, th.sizer))
            {
                alpha = 360 - alpha; chamx = true;
            }
            //XET CHAM VOI CAC MEP CUA THANH CHAN NGANG:
            else if (hitngang(alpha, x, y, th.xn, ydau, size, th.sized, th.sizer) || hitngang(alpha, x, y, th.xn, ycuoi, size, th.sized, th.sizer)
                || hitdoc(x, y, th.xn, ydau, size, th.sized, th.sizer) || hitdoc(x, y, th.xn, ycuoi, size, th.sized, th.sizer))
            {
                if (hitngang(alpha, x, y, th.xn, ydau, size, th.sized, th.sizer) || hitdoc(x, y, th.xn, ydau, size, th.sized, th.sizer))
                    if (x < th.xn + th.sized / 2) alpha = 225;
                    else alpha = 315;
               
                if (hitngang(alpha, x, y, th.xn, ycuoi, size, th.sized, th.sizer) || hitdoc(x, y, th.xn, ycuoi, size, th.sized, th.sizer))
                    if (x < th.xn + th.sized / 2) alpha = 135;
                    else alpha = 45;
            }

            if (hitdoc(x, y, xdau, th.yd + 15, size, th.sizer, th.sized - 30) 
                || hitdoc(x, y, xcuoi, th.yd + 15, size, th.sizer, th.sized - 30))
            {
                alpha = 180 - alpha; chamy = true;
            }
            //XET CHAM VOI CAC MEP CUA THANH CHAN DOC:
            else if (hitdoc(x, y, xdau, th.yd, size, th.sizer, th.sized) || hitdoc(x, y, xcuoi, th.yd, size, th.sizer, th.sized)
                || hitngang(alpha, x, y, xdau, th.yd, size, th.sizer, th.sized) || hitngang(alpha, x, y, xcuoi, th.yd, size, th.sizer, th.sized))
            {
                if (hitdoc(x, y, xdau, th.yd, size, th.sizer, th.sized) || hitngang(alpha, x, y, xdau, th.yd, size, th.sizer, th.sized))
                    if (y < th.yd + th.sized / 2) alpha = 45;
                    else alpha = 315;
                if (hitdoc(x, y, xcuoi, th.yd, size, th.sizer, th.sized) || hitngang(alpha, x, y, xcuoi, th.yd, size, th.sizer, th.sized))
                    if (y < th.yd + th.sized / 2) alpha = 135;
                    else alpha = 225;
            }
            //cho den khi no ra khoi thanh chan hoan toan
            while (inblock(x, y, xdau, th.yd, size, th.sizer, th.sized) || inblock(x, y, xcuoi, th.yd, size, th.sizer, th.sized)
                || inblock(x, y, th.xn, ydau, size, th.sized, th.sizer) || inblock(x, y, th.xn, ycuoi, size, th.sized, th.sizer))
            {
                y -= -sin(alpha0 / 180.0 * 3.14) * dt;
                x -= cos(alpha0 / 180.0 * 3.14) * dt;
            }
        }
        

        //xet cham voi cac block
        bool cham = false; // kiem tra xem ball cham vao block hay chua (dung de xac dinh cham 1 block hay 2 block cung luc?)
        for (int i = 0; i < MAXBLOCKx; i++)
            for (int j = 0; j < MAXBLOCKy; j++)
            {
                if (blo[i][j].no != 0)
                    if (hitngang(alpha, x, y, blo[i][j].x, blo[i][j].y, size, blo[i][j].sized, blo[i][j].sizer) == true)
                    {
                        if (blo[i][j].no0 > 0 && cham == false)
                            if (get_item[2] == false || (get_item[2] == true && (blo[i][j].no >= 4 && blo[i][j].no <= 5))) alpha = 360 - alpha;
                        goto hit;
                    }
                    else if (hitdoc(x, y, blo[i][j].x, blo[i][j].y, size, blo[i][j].sized, blo[i][j].sizer) == true)
                    {
                        if (blo[i][j].no0 > 0 && cham == false)
                            if (get_item[2] == false || (get_item[2] == true && (blo[i][j].no >= 4 && blo[i][j].no <= 5))) alpha = 180 - alpha;
                        goto hit;
                    }
                continue;
            hit:
                cham = true;
                if (blo[i][j].no == -1) { get_item[0] = true; blo[i][j].no = 0; }
                else if (blo[i][j].no == -2) { get_item[1] = true; blo[i][j].no = 0; t_big = time(0); }
                else if (blo[i][j].no == -3) { get_item[2] = true; blo[i][j].no = 0; t_super = time(0); }
                else if (blo[i][j].no == -4) 
                { heart++; print_image(LoadImage("heart.png"), g_screen, heart * 20, 10); blo[i][j].no = 0;}
                else if (blo[i][j].no == 4 || blo[i][j].no == 5) blo[i][j].display();
                else if (blo[i][j].no == 6) blo[i][j].no = 0;
                else blo[i][j].no--;

                if (get_item[1] == true) blo[i][j].no = 0; //khi ball phong to thi co the pha het cac block trong 1 hit
                
                blo[i][j].display();
                if (blo[i][j].no == 0)
                {
                    if ((blo[i][j].no0 >= 1 && blo[i][j].no0 <= 3) || (blo[i][j].no0 >= 4 && blo[i][j].no0 <= 7)) blo[i][j].broke_effect = true;
                    else blo[i][j].edisplay(); 
                }

                //cho den khi no ra khoi block hoan toan
                while ((inblock(x, y, blo[i][j].x, blo[i][j].y, size, blo[i][j].sized, blo[i][j].sizer) == true) && (get_item[2] == false)
                    && blo[i][j].no != 0)
                {
                    y -= -sin(alpha0 / 180.0 * 3.14) * dt;
                    x -= cos(alpha0 / 180.0 * 3.14) * dt;
                }
            }
        //xet cham voi cac teleblock
        for (int i = 0; i < sotele; i++)
        {
            if (hitngang(alpha, x, y, tele[i].x, tele[i].y, size, tele[i].sized, tele[i].sizer) == true)
            {
                if (i % 2 == 1) //cham khoi teleport mau do
                    if (int(y) >= tele[i].y + tele[i].sizer - 5 && int(y) <= tele[i].y + tele[i].sizer)
                    {
                        x = tele[i - 1].x + (x - tele[i].x);
                        //tranh x bi ra ngoai vung teleport
                        if (x <= tele[i - 1].x) x = tele[i - 1].x + 1;
                        else if (x + size >= tele[i - 1].x + tele[i - 1].sized) x = tele[i - 1].x + tele[i - 1].sized - size - 1;
                        y = tele[i - 1].y - size - 1;
                    }
                    else alpha = 360 - alpha;
                if (i % 2 == 0) //cham khoi teleport mau xanh
                    if (int(y) + size >= tele[i].y && int(y) + size <= tele[i].y + 5)
                    {
                        x = tele[i + 1].x + (x - tele[i].x);
                        //tranh x bi ra ngoai vung teleport
                        if (x <= tele[i + 1].x) x = tele[i + 1].x + 1;
                        else if (x + size >= tele[i + 1].x + tele[i + 1].sized) x = tele[i + 1].x + tele[i + 1].sized - size - 1;
                        y = tele[i + 1].y + tele[i + 1].sizer + 1;
                    }
                    else alpha = 360 - alpha;
            }
            else if (hitdoc(x, y, tele[i].x, tele[i].y, size, tele[i].sized, tele[i].sizer) == true)
            {
                alpha = 180 - alpha;
            }
            //cho den khi ra khoi teleblock hoan toan
            while (inblock(x, y, tele[i].x, tele[i].y, size, tele[i].sized, tele[i].sizer) == true)
            {
                y -= -sin(alpha0 / 180.0 * 3.14) * dt*3;
                x -= cos(alpha0 / 180.0 * 3.14) * dt*3;
            }
        }
        // xet cham voi cac quai vat
        for (int i = 0; i < somon; i++)
            if (mon[i].no > 0)
            {
                if (hitngang(alpha, x, y, mon[i].x, mon[i].y, size, mon[i].sized, mon[i].sizer) == true)
                {
                    alpha = 360 - alpha;
                    goto hitmon;
                }
                else if (hitdoc(x, y, mon[i].x, mon[i].y, size, mon[i].sized, mon[i].sizer) == true)
                {
                    alpha = 180 - alpha;
                    goto hitmon;
                }
                continue;
            hitmon:
                {
                    //cho den khi ra khoi area quai vat hoan toan
                    while (inblock(x, y, mon[i].x, mon[i].y, size, mon[i].sized, mon[i].sizer) == true)
                    {
                        y -= -sin(alpha0 / 180.0 * 3.14) * dt;
                        x -= cos(alpha0 / 180.0 * 3.14) * dt;
                    }
                    mon[i].hit_effect = true;
                    if (mon[i].no == 2) mon[i].no = 1;
                    if (mon[i].no == 6) mon[i].no = 7;
                    //if (mon[i].no == 7 && mon[i].HP == 10) { mon[i].atk_effect = true; }
                }
            }

        alpha += 360; //de cho alpha > 0
        alpha %= 360;
        alpha0 = alpha;
       
        if ((chamx == true && th.movex == true) || (chamy == true && th.movey == true))
        {
            srand(time(NULL));
            alpha = (alpha - 30) + rand() % (alpha + 30 - (alpha - 30) + 1);
            //cout << "TRUE " << alpha << endl;
        }

        y += -sin(alpha / 180.0 * 3.14) * dt;
        x += cos(alpha / 180.0 * 3.14) * dt;

        //tranh bi random ra ngoai: thi reset nh phan xa voi guong
        if (chamx == true && th.movex == true)
            if ((int(y) >= ydau && int(y) <= ydau + th.sizer) || (int(y) + size >= ycuoi && int(y) + size <= ycuoi + th.sizer))
            {
                y += sin(alpha / 180.0 * 3.14) * dt;
                alpha = alpha0;
                y += -sin(alpha / 180.0 * 3.14) * dt;
            }
        if (chamy == true && th.movey == true)
            if ((int(x) >= xdau && int(x) <= xdau + th.sizer) || (int(x) + size >= xcuoi && int(x) + size <= xcuoi + th.sizer))
            {
                x -= cos(alpha / 180.0 * 3.14) * dt;
                alpha = alpha0;
                x += cos(alpha / 180.0 * 3.14) * dt;
            }
    }
};
ball b[MAXball];

void bullet_burst() // neu dan dam trung cac block thi bien mat
{
    for (int k = 0; k < 8; k++)
        if (bu[k].x != 0 && bu[k].y != 0)
        {
            for (int i = 0; i < MAXBLOCKx; i++)
                for (int j = 0; j < MAXBLOCKy; j++)
                    if (blo[i][j].no != 0)
                        if ((hitngang(bu[k].alpha, float(bu[k].x), float(bu[k].y), blo[i][j].x, blo[i][j].y, bu[k].size, blo[i][j].sized, blo[i][j].sizer) == true)
                            || (hitdoc(float(bu[k].x), float(bu[k].y), blo[i][j].x, blo[i][j].y, bu[k].size, blo[i][j].sized, blo[i][j].sizer) == true))
                            delete_bullet(k);

            if ((hitngang(bu[k].alpha, float(bu[k].x), float(bu[k].y), th.xn, ydau, bu[k].size, th.sized, th.sizer) == true)
                || (hitngang(bu[k].alpha, float(bu[k].x), float(bu[k].y), th.xn, ycuoi, bu[k].size, th.sized, th.sizer) == true))
            {
                th.t_freezen = time(0); //_getch();
                delete_bullet(k);
            }
            if ((hitdoc(float(bu[k].x), float(bu[k].y), xdau, th.yd, bu[k].size, th.sizer, th.sized) == true)
                || (hitdoc(float(bu[k].x), float(bu[k].y), xcuoi, th.yd, bu[k].size, th.sizer, th.sized) == true))
            {
                th.t_freezed = time(0);
                delete_bullet(k);
            }
            for (int i = 0; i < soball; i++)
                if ((hitngang(bu[k].alpha, float(bu[k].x), float(bu[k].y), b[i].x, b[i].y, bu[k].size, b[i].size, b[i].size) == true)
                    || (hitdoc(float(bu[k].x), float(bu[k].y), b[i].x, b[i].y, bu[k].size, b[i].size, b[i].size) == true))
                {
                    delete_bullet(k);
                    srand(time(NULL));
                    b[i].alpha = rand() % 360;
                }

            for (int i = 0; i < sotele; i++)
            {
                if (hitdoc(float(bu[k].x), float(bu[k].y), tele[i].x, tele[i].y, bu[k].size, tele[i].sized, tele[i].sizer) == true)
                    delete_bullet(k);
                else if (hitngang(bu[k].alpha, float(bu[k].x), float(bu[k].y), tele[i].x, tele[i].y, bu[k].size, tele[i].sized, tele[i].sizer) == true)
                {
                    bu[k].edisplay();
                    if (i % 2 == 1)
                        if (bu[k].y >= tele[i].y + tele[i].sizer - 2 && bu[k].y <= tele[i].y + tele[i].sizer)
                        {
                            bu[k].x = tele[i - 1].x + (bu[k].x - tele[i].x);
                            bu[k].y = tele[i - 1].y - bu[k].size - 1;
                        }
                    if (i % 2 == 0)
                        if (bu[k].y + bu[k].size >= tele[i].y && bu[k].y + bu[k].size <= tele[i].y + 2)
                        {
                            bu[k].x = tele[i + 1].x + (bu[k].x - tele[i].x);
                            bu[k].y = tele[i + 1].y + tele[i + 1].sizer + 1;
                        }
                    bu[k].xf = float(bu[k].x);
                    bu[k].yf = float(bu[k].y);
                }
            }
            if (int(bu[k].yf) <= 25) delete_bullet(k); //tranh cham vao thanh HP phia tren man hinh
        }
}
bool clearblock()
{
    for (int i = 0; i < MAXBLOCKx; i++)
        for (int j = 0; j < MAXBLOCKy; j++)
            if (blo[i][j].no != 4 && blo[i][j].no != 5 && blo[i][j].no > 0) return false;
    return true;
}
bool clearmon()
{
    for (int i = 0; i < somon; i++)
        if (mon[i].no != 0) return false;
    return true;
}

void intro()
{
    SDL_Event g_intro;
    bool is_quit = false;
    if (Init() == false)
        return;
    int y = 700;
    while (!is_quit)
    {
        while (SDL_PollEvent(&g_trash))
        {
            if (g_trash.type == SDL_QUIT)
            {
                is_quit = true;
                break;
            }
        }
        print_image(LoadImage("intro.png"), g_screen, 0, y);
        if (y>0) y-=5;
        else { SDL_Delay(1000); break; }
        if (SDL_Flip(g_screen) == -1)
            return;
    }

    print_image(LoadImage("1player.png"), g_screen, 530, 400);
    bool kt = false; //kiem tra nut bam lua chon co bi de ko

    while (!is_quit)
    {
        while (SDL_PollEvent(&g_intro))
        {
            if (g_intro.type == SDL_QUIT)
            {
                is_quit = true;
                break;
            }
        }

        if (g_intro.type == SDL_KEYDOWN)
            if ((kt == false) && (g_intro.key.keysym.sym == SDLK_w || g_intro.key.keysym.sym == SDLK_s))
            {
                multiplay = !multiplay;
                kt = true;
            }
        if (g_intro.type == SDL_KEYUP) kt = false;

        if (multiplay == true) print_image(LoadImage("2player.png"), g_screen, 530, 400);
        else print_image(LoadImage("1player.png"), g_screen, 530, 400);
        if (g_intro.key.keysym.sym == SDLK_SPACE) break;
        if (SDL_Flip(g_screen) == -1)
            return;
    }
}
void loading()
{
    bool is_quit = false;
    if (Init() == false)
        return;
    long t = time(0);
    print_image(LoadImage("loading.png"), g_screen, 0, 0);
    mon[0].no = 2;
    mon[0].x = 570; mon[0].y = 280;
    while (!is_quit)
    {
        while (SDL_PollEvent(&g_trash))
        {
            if (g_trash.type == SDL_QUIT)
            {
                is_quit = true;
                break;
            }
        }

        mon[0].display();
        SDL_Delay(5);
        if (time(0) - t >= 6) break;
        if (SDL_Flip(g_screen) == -1)
            return;
    }
}
void stageintro(int stage)
{
    int y = -50;
    bool xuong = true;
    while (1)
    {
        while (SDL_PollEvent(&g_trash))
        {/*xoa cac phim nhan rac*/}

        if (stage == 0) print_image(LoadImage("stageclear.png"), g_screen, 500, y);
        if (stage == 1) print_image(LoadImage("stage1.png"), g_screen, 500, y);
        if (stage == 2) print_image(LoadImage("stage2.png"), g_screen, 500, y);
        if (stage == 3) print_image(LoadImage("stage3.png"), g_screen, 500, y);
        if (stage == 4) print_image(LoadImage("stagemidboss.png"), g_screen, 500, y);
        if (stage == 5) print_image(LoadImage("stage5.png"), g_screen, 500, y);
        if (stage == 6) print_image(LoadImage("stage6.png"), g_screen, 500, y);
        if (stage == 7) print_image(LoadImage("stage7.png"), g_screen, 500, y);
        if (stage == 8) print_image(LoadImage("stageboss.png"), g_screen, 500, y);
        if (stage == 9) print_image(LoadImage("stageextra.png"), g_screen, 500, y);


        if (xuong == true) y++;
        else y--;
        if (y == 0) 
        {
            if (stage == 0)
            {
                Mix_HaltMusic();
                Mix_PlayChannel(-1, sound[0], 0);
                SDL_Delay(4000);
            }
            else SDL_Delay(1500); 
            xuong = false; 
        }
        if (y < -55) break;

        SDL_Delay(1);
        if (SDL_Flip(g_screen) == -1)
            return;
    }
}
void continu()
{
    Mix_HaltMusic();
    Mix_PlayMusic(loadmusic, 0);

    SDL_Event g_intro;
    while (SDL_PollEvent(&g_trash))
    {}
    print_image(LoadImage("continue.png"), g_screen, 0, 0);
    print_image(LoadImage("continueY.png"), g_screen, 530, 320);
    bool kt = false; //kiem tra nut bam lua chon co bi de ko

    while (1)
    {
        while (SDL_PollEvent(&g_intro))
        {
            if (g_intro.type == SDL_QUIT)
            {}
        }

        if (g_intro.type == SDL_KEYDOWN)
            if ((kt == false) && (g_intro.key.keysym.sym == SDLK_a || g_intro.key.keysym.sym == SDLK_d))
            {
                kt_conti = !kt_conti;
                kt = true;
            }
        if (g_intro.type == SDL_KEYUP) kt = false;

        if (kt_conti == true) print_image(LoadImage("continueY.png"), g_screen, 530, 320);
        else print_image(LoadImage("continueN.png"), g_screen, 530, 320);
        if (g_intro.key.keysym.sym == SDLK_SPACE) break;
        if (SDL_Flip(g_screen) == -1)
            return;
    }
    print_image(LoadImage("bkground.png"), g_screen, 0, 0);
}
void credit()
{
    Mix_HaltMusic();
    Mix_PlayMusic(creditmusic, 0);
    SDL_Event g_intro;
    print_image(LoadImage("bkground.png"), g_screen, 0, 0);
    while (SDL_PollEvent(&g_trash))
    {}

    int y = SCREEN_HEIGHT;
    while (1)
    {
        while (SDL_PollEvent(&g_intro))
        {
            if (g_intro.type == SDL_QUIT)
            {
                return;
            }
        }

        print_image(LoadImage("credit.png"), g_screen, 0, y);
        //SDL_Delay(10);
        y-=3;

        if (SDL_Flip(g_screen) == -1)
            return;
    }
}

//=========================================================================================================

//=======================================================================================================

int main()
{
    
reset:
    bool is_quit = false;
    if (Init() == false)
        return 0;
    if (font == NULL)
        cout << "NULL";
    
    //Mix_PlayChannel(-1, music0, 0);

    Mix_PlayMusic(bkmusic, -1);
    intro();
    //Mix_PlayChannel(-1, music, 0);

    b[0].dt = 1; th.sized = 100;
    stage = 0;
    heart = 7;
    socontinue = 0;
nextstage:
    stage++;
revive:
    th.sized = 100;
    Mix_HaltMusic();
    Mix_PlayMusic(loadmusic, 0);
    loading();
    Mix_HaltMusic();

    print_image(LoadImage("bkground.png"), g_screen, 0, 0);
    soitemdrop = 0; soball = 1;
    ifstream infile;
    if (stage == 1) { infile.open("stage1.txt"); Mix_PlayMusic(stagemusic[0], -1);}
    if (stage == 2) { infile.open("stage2.txt"); Mix_PlayMusic(stagemusic[0], -1);}
    if (stage == 3) { infile.open("stage3.txt"); Mix_PlayMusic(stagemusic[1], -1); }
    if (stage == 4) { infile.open("stagemidboss.txt"); Mix_PlayMusic(stagemusic[4], -1); }
    if (stage == 5) { infile.open("stage5.txt"); Mix_PlayMusic(stagemusic[2], -1); }
    if (stage == 6) { infile.open("stage6.txt"); Mix_PlayMusic(stagemusic[3], -1); }
    if (stage == 7) { infile.open("stage7.txt"); Mix_PlayMusic(stagemusic[2], -1); }
    if (stage == 8) { infile.open("stageboss.txt"); Mix_PlayMusic(stagemusic[4], -1); }
    if (stage == 9)
    {
        Mix_PlayMusic(victorymusic, 0);
        print_image(LoadImage("gamewin.png"), g_screen, 0, 0);
        SDL_Flip(g_screen);
        SDL_Delay(13500);
        print_image(LoadImage("bkground.png"), g_screen, 0, 0);
        if (socontinue <= 0)
        {
            b[0].dt = 1; th.sized = 100; heart = 10;
            infile.open("stageextra.txt"); //Mix_PlayMusic(stagemusic[4], -1);
            Mix_PlayMusic(stagemusic[6], -1);
            playextra = true;
            socontinue = -1;
        }
        else stage++;
    }
    if (stage >= 10)
    {
        if (playextra == false)
        {
            Mix_PlayMusic(victorymusic, 0);
            print_image(LoadImage("gamewin.png"), g_screen, 0, 0);
            SDL_Flip(g_screen);
            SDL_Delay(13500);
        }
        credit();
    }
    //ifstream infile("in.txt");
    //THIET LAP BLOCK/ITEM:
    for (int j = 0; j < MAXBLOCKy-1; j++)
        for (int i = 0; i < MAXBLOCKx; i++)
        {
            infile >> blo[i][j].no;
            blo[i][j].no0 = blo[i][j].no;
            if (blo[i][j].no != 0)
            {
                {
                    blo[i][j].x = 300 + i * 50;
                    blo[i][j].y = 150 + j * 40;
                }
                if (blo[i][j].no < 0)
                {
                    blo[i][j].sizer = 20;
                    blo[i][j].sized = 20;
                    blo[i][j].x = 300 + i * 50 + 10;
                    blo[i][j].y = 150 + j * 40 + 10;
                }
                if (blo[i][j].no > 0 && blo[i][j].no <= 3)
                {
                    blo[i][j].sizer = 20;
                    blo[i][j].sized = 100;
                }
                if (blo[i][j].no >= 4 && blo[i][j].no <= 7)
                {
                    blo[i][j].sizer = 40;
                    blo[i][j].sized = 40;
                    if (blo[i][j].no == 5) blo[i][j].x = 300 + i * 50 + 10;
                }
                blo[i][j].display(); SDL_Flip(g_screen);
            }
            else { blo[i][j].x = 0; blo[i][j].y = 0; }
        }
    for (int i = 0; i < MAXBLOCKx; i++) blo[i][MAXBLOCKy-1].no = 0;

    //THIET LAP QUAI VAT/ TELEBLOCK:
    somon = 0;
    sotele = 0;
    while (!infile.eof())
    {
        infile >> mon[somon].no >> mon[somon].x0 >> mon[somon].y0 >> mon[somon].speed >> mon[somon].dichuyen;
        mon[somon].start(mon[somon].x0, mon[somon].y0, mon[somon].dichuyen);
        if (mon[somon].no >= 1 && mon[somon].no <= 3) mon[somon].HP = 2;
        if (mon[somon].no == 4) mon[somon].HP = 3;
        if (mon[somon].no >= 1 && mon[somon].no <= 4) { mon[somon].sized = 40; mon[somon].sizer = 30; }
        if (mon[somon].no == 5) { mon[somon].sized = 40; mon[somon].sizer = 40; mon[somon].HP = 3; }
        if (mon[somon].no == 6) 
        { 
            mon[somon].sized = 100; mon[somon].sizer = 60; mon[somon].HP = 20; 
            print_image(LoadImage("HPboss.png"), g_screen, xHPboss, yHPboss); SDL_Flip(g_screen);
        }
        if (mon[somon].no == 9)
        {
            mon[somon].sized = 80; mon[somon].sizer = 80; mon[somon].HP = 5;
            print_image(LoadImage("HPmidboss.png"), g_screen, xHPboss, yHPboss); SDL_Flip(g_screen);
        }
        if (mon[somon].no == 10) 
        { 
            mon[somon].sized = 60; mon[somon].sizer = 90; mon[somon].HP = 10; 
            print_image(LoadImage("HPghost.png"), g_screen, xHPboss, yHPboss); SDL_Flip(g_screen);
        }
        if (mon[somon].no < 0)
        {
            tele[sotele].x = mon[somon].x0;
            tele[sotele].y = mon[somon].y0;
            tele[sotele].display(sotele); SDL_Flip(g_screen);
            sotele++;
        }
        if (mon[somon].no > 0) 
        { 
            mon[somon].x = mon[somon].x0; mon[somon].y = mon[somon].y0; 
            mon[somon].display(); SDL_Flip(g_screen);
            somon++; 
        }
    }
    //cout << "somon:" << somon << endl;

    infile.close();

    stageintro(stage);

    bool dieup = false, dieright = false, dieleft = false, diedown = true;// kiem tra xem ball ra ngoai o phia nao
    /*g_bkground = LoadImage("bkground.png");
    if (g_bkground == NULL)
    {
        return 0;
    }
    print_image(g_bkground, g_screen, 0, 0);*/
    while (heart > 0)
    {
        //mon[0].hit_effect == true;
        //mon[0].hiteffect();
        int t0 = 0; //bien thoi gian luc chon huong de ban ball ra khoi thanh
        get_item[0] = false;
        get_item[1] = false;
        get_item[2] = false; b[0].size = 10;
        if (stage != 7) b[0].dt = 1;
        else b[0].dt = 1.2;
        th.t_freezed = 0; th.t_freezen = 0; th.t_reverse = 0;
        soball = 1;
        //for (int j = 0; j < soball; j++) { b[j].size = 10; b[j].eedisplay(); } //xoa cac du anh
        for (int i = 1; i <= heart; i++) print_image(LoadImage("heart.png"), g_screen, i * 20, 10); //in so heart

        for (int j = 0; j < MAXBLOCKy; j++) // block+item
            for (int i = 0; i < MAXBLOCKx; i++) blo[i][j].display();
        for (int i = 0; i < sotele; i++) tele[i].display(i); // in cac khoi teleport
        for (int i = 0; i < 5; i++) { b[0].sdx[i] = 0; b[0].sdy[i] = 0; } //tranh in cac dom den cua du anh ko can thiet

        while (!is_quit) //LUC CHUA BAN BALL RA HOI THANH:
        {
            t0++;
            if (t0 >= 1000) t0 = 0;
            while (SDL_PollEvent(&g_even))
            {
                if (g_even.type == SDL_QUIT)
                {
                    is_quit = true;
                    break;
                }
            }

            for (int i = 0; i < 8; i++) //in bullet
                if (!(bu[i].x == 0 && bu[i].y == 0))
                {
                    bu[i].move();
                    bu[i].display();
                }
            bullet_burst();

            for (int i = 0; i < somon; i++) // in quai vat trong khi chon huong ban ball
                if (mon[i].HP > 0)
                {
                    if (mon[i].hit_effect == true) mon[i].hiteffect();
                    else if (mon[i].atk_effect == true) mon[i].atkeffect();
                    else
                    {
                        mon[i].move();
                        mon[i].display();
                    }
                    if (mon[i].HP <= 0) 
                    { 
                        if (mon[i].no == 9 || mon[i].no == 8) mon[i].edisplay();
                        mon[i].no = 0; 
                    }
                }

            //CHON HUONG BAN BALL:
            b[0].edisplay();
            if (diedown || dieup)
            {
                b[0].x = th.xn + th.sized / 2;
                if (diedown) b[0].y = ycuoi - b[0].size - 1;
                if (dieup) b[0].y = ydau + th.sizer + 1;
            }
            if (dieleft || dieright)
            {
                b[0].y = th.yd + th.sized / 2;
                if (dieleft) b[0].x = xdau + th.sizer + 1;
                if (dieright) b[0].x = xcuoi - b[0].size - 1;
            }
            th.edisplay();
            th.move();
            th.display();

            b[0].display();
            ////////

            if (diedown == true)
            {
                if (t0 % 200 == 0) b[0].alpha = 30;
                if (t0 % 200 == 50) b[0].alpha = 60;
                if (t0 % 200 == 100) b[0].alpha = 120;
                if (t0 % 200 == 150) b[0].alpha = 150;
            }
            if (dieup == true)
            {
                if (t0 % 200 == 0) b[0].alpha = 210;
                if (t0 % 200 == 50) b[0].alpha = 240;
                if (t0 % 200 == 100) b[0].alpha = 300;
                if (t0 % 200 == 150) b[0].alpha = 330;
            }
            if (dieleft == true)
            {
                if (t0 % 200 == 0) b[0].alpha = 300;
                if (t0 % 200 == 50) b[0].alpha = 330;
                if (t0 % 200 == 100) b[0].alpha = 30;
                if (t0 % 200 == 150) b[0].alpha = 60;
            }
            if (dieright == true)
            {
                if (t0 % 200 == 0) b[0].alpha = 240;
                if (t0 % 200 == 50) b[0].alpha = 210;
                if (t0 % 200 == 100) b[0].alpha = 150;
                if (t0 % 200 == 150) b[0].alpha = 120;
            }

            if (g_even.type == SDL_KEYDOWN)
                if (g_even.key.keysym.sym == SDLK_SPACE) break; //neu nhan phim SPACE thi ban ball ra khoi thanh

            b[1].edisplay();
            b[1].y = b[0].y - sin(b[0].alpha / 180.0 * 3.14) * 20;
            b[1].x = b[0].x + cos(b[0].alpha / 180.0 * 3.14) * 20;
            b[1].display(1);

            if (SDL_Flip(g_screen) == -1)
                return 0;
        }
        b[1].edisplay();

        //---------------------------------------------------------------------------------------
        while (!is_quit && soball > 0)
        {
            while (SDL_PollEvent(&g_even))
            {
                if (g_even.type == SDL_QUIT)
                {
                    is_quit = true;
                    break;
                }
            }

            th.edisplay();
            th.move();
            th.display();
            cout << "A";
            /*SDL_Color backgroundColor = { 0, 0, 255 };
            if (font!=NULL)
            cout << font;
            SDL_Surface* textSurface = TTF_RenderText_Solid(font, "This is my text.", White);
            cout << "C";
            SDL_Rect textLocation = { 100, 100, 0, 0 };
            cout << "D";
            SDL_BlitSurface(textSurface, NULL, g_screen, &textLocation);
            cout << "E";*/
            for (int i = 0; i < 8; i++) //in bullet
                if (!(bu[i].x == 0 && bu[i].y == 0))
                {
                    bu[i].move();
                    bu[i].display();
                }

            for (int i = 0; i < somon; i++)
                if (mon[i].HP > 0)
                {
                    if (mon[i].hit_effect == true) mon[i].hiteffect();
                    else if (mon[i].atk_effect == true) mon[i].atkeffect();
                    else
                    {
                        //if (mon[i].no == 8) mon[i].edisplay();
                        mon[i].move();
                        mon[i].display();
                    }
                    if (mon[i].HP <= 0) 
                    { 
                        if (mon[i].no == 8 || mon[i].no == 9) mon[i].edisplay();
                        mon[i].no = 0; 
                    }
                }

            for (int j = 0; j < MAXBLOCKy; j++)
                for (int i = 0; i < MAXBLOCKx; i++)
                    if (blo[i][j].broke_effect == true) blo[i][j].broke();


            for (int i = 0; i < soball; i++)
                if (b[i].x >= xdau - 20 && b[i].x <= xcuoi + 20 && b[i].y >= ydau - 20 && b[i].y <= ycuoi + 20) // khi ball chua ra ngoai
                {
                    b[i].edisplay();
                    b[i].move();
                    //cout << get_item;
                    if (get_item[0] == true && soball < MAXball) //an duoc vat pham x2 ball
                    {
                        soball++;
                        b[soball - 1].x = b[i].x;
                        b[soball - 1].y = b[i].y;
                        b[soball - 1].alpha = b[i].alpha - 30;
                        b[i].alpha += 30;

                        get_item[0] = false;
                    }
                    if (get_item[1] == true) //an duoc vat pham phong to
                    {
                        b[i].dt = 1.5; //tang toc do
                        b[i].size = 20; //tang kich thuoc
                        //t_big++;
                        if (time(0) - t_big >= 10)
                        {
                            get_item[1] = false; //t_big = 0; 
                            for (int j = 0; j < soball; j++) { b[j].size = 10; b[j].dt = 1; b[j].eedisplay(); }
                        }
                    }
                    if (get_item[2] == true)
                    {
                        if (get_item[1] == true)
                            for (int j = 0; j < soball; j++) b[j].eedisplay();
                        b[i].dt = 1;
                        b[i].size = 10;
                        get_item[1] = false;
                        if (time(0) - t_super >= 9) get_item[2] = false;
                    }
                    b[i].display();
                }
                else // neu ball ra ngoai thi xoa di 1 ball
                {
                    b[i].eedisplay();
                    if (soball > 1) //gan cac gia tri cua ball cuoi cung cho ball da ra ngoai roi xoa ball cuoi cung
                    {
                        b[i] = b[soball - 1];
                        //b[soball - 1].x = 0; b[soball - 1].y = 0;
                    }
                    soball--;
                }

            bullet_burst();

            if (soball == 1) th.speed = 2;
            if (soball == 2) th.speed = 3;
            if (soball >= 3) th.speed = 4; //tang toc do thanh chan khi co nhieu ball do su giam hieu suat

            if (soball == 0)
            {
                dieleft = false; dieright = false; dieup = false; diedown = false;
                if (b[0].x < xdau) dieleft = true;
                if (b[0].x > xcuoi) dieright = true;
                if (b[0].y < ydau) dieup = true;
                if (b[0].y > ycuoi) diedown = true;
            }

            //CleanUp();
            //SDL_Delay(1);
            if (SDL_Flip(g_screen) == -1)
                return 0;

            if (stage != 4 && stage != 6 && stage != 8 && stage != 9)
            {
                if (clearblock()) //neu ph het cac block co the pha
                {
                    t_clear++;
                    if (t_clear >= 200) { t_clear = 0; stageintro(0); goto nextstage; }
                }
            }
            else if (clearmon())
            {
                t_clear++;
                if (t_clear >= 200) { t_clear = 0; stageintro(0); goto nextstage; }
            }
        }

        //Mix_PauseMusic();
        b[0].broke();
        print_image(LoadImage("eitem.png"), g_screen, heart * 20, 10);
        heart--;

        for (int j = 0; j < soball; j++) { b[j].size = 10; b[j].eedisplay(); } //xoa cac du anh
        //Mix_ResumeMusic();
    }

    if (socontinue <= 0)
    {
        continu();
        if (kt_conti == true) { heart = 5; socontinue++; goto revive; }
    }

    Mix_HaltMusic();
    Mix_PlayMusic(gameovermusic, 0);
    if (stage==9) print_image(LoadImage("gameover2.png"), g_screen, 0, 0);
    else print_image(LoadImage("gameover.png"), g_screen, 0, 0);
    SDL_Flip(g_screen);
    SDL_Delay(4000);

    Mix_HaltMusic();
    goto reset;
    //CleanUp();
    SDL_Quit();
    return 1;
}