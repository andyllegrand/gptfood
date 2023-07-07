//
//  Service.swift
//  gptfood
//
//  Created by Andy LeGrand on 6/20/23.
//

import Foundation

//  Stores state for the entire app. Manages calls to backend
class Service: ObservableObject {
    @Published public private(set) var ingredients: [Ingredient]
    @Published public private(set) var recipes: [Recipe]
    @Published public private(set) var loading_recipes: Bool
    
    private var config: Settings
    
    init() {
        let decoder = JSONDecoder()
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        
        //  Pull settings from json
        let settingsPath = documentsPath.appendingPathComponent("settings.json")
        config = Settings(server_ip: "http://192.168.1.27")

        
        //  Pull previous recipes and ingredients from json
        
        
        ingredients = []
        recipes = []
        loading_recipes = false
    }
    
    //  Sets the ingredients list to a new list
    func addIngredient(new_ingredient: Ingredient) {
        ingredients.append(new_ingredient)
    }
    
    func removeIngredient(at index: Int) {
        ingredients.remove(at: index)
    }
    
    func updateRecipes() {
        //  Encode ingredients list into JSON
        guard let postData = try? JSONEncoder().encode(ingredients) else {
            print("Failed to encode ingredients to JSON")
            return
        }
        
        //  Build request
        let url = URL(string: (config.server_ip + "/recipe"))!
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
    }
}
