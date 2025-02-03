#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <iostream>
#include <string>
#include <csignal>

const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;
bool running = true; // Global flag for the main loop

void RenderText(SDL_Renderer* renderer, TTF_Font* font, const std::string& text, int x, int y, SDL_Color color) {
    SDL_Surface* surface = TTF_RenderText_Solid(font, text.c_str(), color);
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);

    SDL_Rect dstRect = {x, y, surface->w, surface->h};
    SDL_RenderCopy(renderer, texture, nullptr, &dstRect);

    SDL_FreeSurface(surface);
    SDL_DestroyTexture(texture);
}

// Signal handler for Ctrl+C
void handleSigint(int) {
    running = false;
}

int main() {
    // Set up signal handling for Ctrl+C
    std::signal(SIGINT, handleSigint);

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "Failed to initialize SDL: " << SDL_GetError() << "\n";
        return -1;
    }

    if (TTF_Init() < 0) {
        std::cerr << "Failed to initialize SDL_ttf: " << TTF_GetError() << "\n";
        SDL_Quit();
        return -1;
    }

    SDL_Window* window = SDL_CreateWindow("Simple CAD",
                                          SDL_WINDOWPOS_CENTERED,
                                          SDL_WINDOWPOS_CENTERED,
                                          WINDOW_WIDTH, WINDOW_HEIGHT,
                                          SDL_WINDOW_SHOWN);
    if (!window) {
        std::cerr << "Failed to create window: " << SDL_GetError() << "\n";
        SDL_Quit();
        return -1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Failed to create renderer: " << SDL_GetError() << "\n";
        SDL_DestroyWindow(window);
        SDL_Quit();
        return -1;
    }

    TTF_Font* font = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16);
    if (!font) {
        std::cerr << "Failed to load font: " << TTF_GetError() << "\n";
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return -1;
    }

    SDL_Event event;

    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Clear screen
        SDL_RenderClear(renderer);

        // Draw X-Y plane in light gray
        SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255); // Light gray color
        SDL_Rect xyPlane = {100, 100, 600, 400}; // Define the plane rectangle
        SDL_RenderFillRect(renderer, &xyPlane);

        // Draw X, Y, and Z axes
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // X-axis: Red
        SDL_RenderDrawLine(renderer, 100, 300, 700, 300);

        //SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255); // Y-axis: Green
       // SDL_RenderDrawLine(renderer, 400, 500, 400, 100);
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255); // Z-axis: Blue
        SDL_RenderDrawLine(renderer, 400, 300, 550, 150);
        


//SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255); // Z-axis: Blue
      //  SDL_RenderDrawLine(renderer, 400, 300, 550, 150);
        SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255); // Y-axis: Green
        SDL_RenderDrawLine(renderer, 400, 500, 400, 100);

        // Draw axis labels
        SDL_Color white = {255, 255, 255, 255};
        RenderText(renderer, font, "+X", 710, 300, white);
        RenderText(renderer, font, "+Z", 400, 80, white);
        RenderText(renderer, font, "+Y", 560, 140, white);

        SDL_RenderPresent(renderer);
    }

    TTF_CloseFont(font);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();

    return 0;
}
