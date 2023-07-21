//
//  Service.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

import Foundation

let debug_no_request : Bool = true

//  Stores state for the entire app. Manages calls to backend
class Service: ObservableObject {
    @Published public private(set) var ingredients: [Ingredient]
    @Published public private(set) var recipes: [Recipe]
    @Published public private(set) var loading_recipes: Bool
    @Published public private(set) var error: String?
    
    private var config: Settings
    
    init() {
        let decoder = JSONDecoder()
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        
        //  Pull settings from json
        let settingsPath = documentsPath.appendingPathComponent("settings.json")
        config = Settings(server_ip: "http://192.168.1.27")
        
        ingredients = []
        recipes = []
        loading_recipes = false
        
        loadData()
        
        //  check directions file
        
    }
    
    //  Sets the ingredients list to a new list
    func addIngredient(new_ingredient: Ingredient) {
        ingredients.append(new_ingredient)
        saveData()
    }
    
    func removeIngredient(at index: Int) {
        ingredients.remove(at: index)
        saveData()
    }
    
    func updateRecipes() {
        //  Check debugdat
        if debug_no_request {
            recipes.append(Recipe(name: "test"))
            saveData()
            return
        }
        
        //  Encode ingredients list into JSON
        guard let postData = try? JSONEncoder().encode(ingredients) else {
            print("Failed to encode ingredients to JSON")
            return
        }
        
        //  Build request
        let url = URL(string: (config.server_ip + "/recipeList"))!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = postData
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        //  Set loading to true and send request
        DispatchQueue.main.async {
            self.loading_recipes = true
        }
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            DispatchQueue.main.async {
                defer { self.loading_recipes = false }

                guard let data = data else { return }
                
                do {
                    // Decode JSON response into array of dictionaries
                    if let jsonArray = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as? [[String: Any]] {
                        // Map array of dictionaries into array of Recipes
                        let new_recipes = jsonArray.compactMap { dict -> Recipe? in
                            if let name = dict["name"] as? String {
                                return Recipe(name: name)
                            } else {
                                return nil
                            }
                        }
                        self.recipes = new_recipes
                    }
                } catch {
                    //  Display error
                    print("Failed to decode JSON")
                }
            }
        }
        task.resume()
        
        saveData()
    }
    
    func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        return paths[0]
    }
    
    func saveData() {
        print("saving data")
        
        let encoder = JSONEncoder()
            if let encodedIngredients = try? encoder.encode(ingredients) {
                let ingredientsUrl = getDocumentsDirectory().appendingPathComponent("ingredients.json")
                try? encodedIngredients.write(to: ingredientsUrl)
            }

            if let encodedRecipes = try? encoder.encode(recipes) {
                let recipesUrl = getDocumentsDirectory().appendingPathComponent("recipes.json")
                try? encodedRecipes.write(to: recipesUrl)
            }
        
        print("done")
    }

    func loadData() {
        print("loading data")
        
        let decoder = JSONDecoder()

        let ingredientsUrl = getDocumentsDirectory().appendingPathComponent("ingredients.json")
        if let data = try? Data(contentsOf: ingredientsUrl),
           let decodedIngredients = try? decoder.decode([Ingredient].self, from: data) {
            ingredients = decodedIngredients
        }

        let recipesUrl = getDocumentsDirectory().appendingPathComponent("recipes.json")
        if let data = try? Data(contentsOf: recipesUrl),
           let decodedRecipes = try? decoder.decode([Recipe].self, from: data) {
            recipes = decodedRecipes
        }
        
        print("done")
    }
    
    func clearDirectionsFile() {
        
    }
    
    func queryBackEndForDirections(recipeName: String) {
        
    }
    
    func queryBackEndForImage(recipeName: String) {
        
    }
    
    func loadRecipeDirections(recipeName: String) {
        //  check file. If matching recipe found do nothing
        
        //  add directions and image to file by querying the backend
        
    }
}
