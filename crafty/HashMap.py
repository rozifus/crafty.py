
"""
* Spatial HashMap for broad phase collision
*
* @author rozifus, translated from [craftyjs]HashMap by Louis Stowasser
*
"""

class HashMap:
    """
    * #Crafty.HashMap.constructor
    * @comp Crafty.HashMap
    * @sign public void Crafty.HashMap([cellsize])
    * @param cellsize - the cell size. If omitted, `cellsize` is 64.
    *
    * Set `cellsize`.
    * And create `this.map`.
    """

    HASH_FORM = "{0} {1}"
    cellsize = None

    def __init__(self, cell=64):
        cellsize = cell
        self.map = {};

    """
    * #Crafty.map.insert
    * @comp Crafty.map
    * @sign public Object Crafty.map.insert(Object obj)
    * @param obj - An entity to be inserted.
    *
    * `obj` is inserted in '.map' of the corresponding broad phase cells. An object of the following fields is returned.
    * ~~~
    * - the object that keep track of cells (keys)
    * - `obj`
    * - the HashMap object
    * ~~~
    """

    def insert(self, obj):
        keys = HashMap.key(obj)
        entry = Entry(keys, obj, self)

        #insert into all x buckets
        for i in range(keys.x1, keys.x2+1):
            #insert into all y buckets
            for j in range(keys.y1, keys.y2+1):
                rhash = HASH_FORM.format(i, j)
                if not self.map.has_key(rhash):
                    self.map[rhash] = [];
                self.map[rhash].append(obj);

        return entry

    """
    * #Crafty.map.search
    * @comp Crafty.map
    * @sign public Object Crafty.map.search(Object rect[, Boolean filter])
    * @param rect - the rectangular region to search for entities.
    * @param filter - Default value is true. Otherwise, must be false.
    *
    * - If `filter` is `false`, just search for all the entries in the give `rect` region by broad phase collision. Entity may be returned duplicated.
    * - If `filter` is `true`, filter the above results by checking that they actually overlap `rect`.
    * The easier usage is with `filter`=`true`. For performance reason, you may use `filter`=`false`, and filter the result yourself. See examples in drawing.js and collision.js
    """

    def search(self, rect, filter=True):
        keys = HashMap.key(rect)
        results = []

        #search in all x buckets
        for i in range(keys.x1, keys.x2+1):
            #insert into all y buckets
            for j in range(keys.y1, keys.y2+1):
                rhash = HASH_FORM.format(i, j)

                if self.map.has_key(rhash):
                    results += self.map[rhash]

        if filter:
            id = None
            finalresult = []
            found = {}
            #add unique elements to lookup table with the entity ID as unique key
            l = len(results)
            for obj in results:
                if (obj == None):
                    continue #skip if deleted
                id = obj[0]; #unique ID

                #check if not added to hash and that actually intersects
                if (not found.has_key(id)) \
                   and obj.x < rect._x + rect._w \
                   and obj._x + obj._w > rect._x \
                   and obj.y < rect._y + rect._h \
                   and obj._h + obj._y > rect._y ):
                        found[id] = results[i]

            #loop over lookup table and copy to final array
            for obj in found:
                finalresult.append(obj)

            return finalresult
        else:
            return results

    """
    /**@
    * #Crafty.map.remove
    * @comp Crafty.map
    * @sign public void Crafty.map.remove([Object keys, ]Object obj)
    * @param keys - key region. If omitted, it will be derived from obj by `Crafty.HashMap.key`.
    * @param obj - need more document.
    *
    * Remove an entity in a broad phase map.
    * - The second form is only used in Crafty.HashMap to save time for computing keys again, where keys were computed previously from obj. End users should not call this form directly.
    *
    * @example
    * ~~~
    * Crafty.map.remove(e);
    * ~~~
    */
    """

    def remove(keys, obj=None):
        if obj == None:
            obj = keys
            keys = HashMap.key(obj)
        }

        #search in all x buckets
        for i in range(keys.x1, keys.x2+1):
            #insert into all y buckets
            for j in range(keys.y1, keys.y2+1):
                rhash = HASH_FORM.format(i,j) ;

                if this.map.has_key(rhash):
                    cell = this.map[hash]
                    n = len(cell)
                    #loop over objs in cell and delete
                    for m in range(n):
                        if cell.has_key(m) and (cell[m][0] == obj[0]):
                            cell.pop(m)

    """
    /**@
    * #Crafty.map.boundaries
    * @comp Crafty.map
    * @sign public Object Crafty.map.boundaries()
    *
    * The return `Object` is of the following format.
    * ~~~
    * {
    *   min: {
    *     x: val_x,
    *     y: val_y
    *   },
    *   max: {
    *     x: val_x,
    *     y: val_y
    *   }
    * }
    * ~~~
    */
    """

    boundaries: function () {
            var k, ent,
            hash = {
                max: { x: -Infinity, y: -Infinity },
                min: { x: Infinity, y: Infinity }
            },
            coords = {
                max: { x: -Infinity, y: -Infinity },
                min: { x: Infinity, y: Infinity }
            };

      //Using broad phase hash to speed up the computation of boundaries.
            for (var h in this.map) {
                if (!this.map[h].length) continue;

        //broad phase coordinate
                var map_coord = h.split(SPACE),
                    i=map_coord[0],
                    j=map_coord[0];
                if (i >= hash.max.x) {
                    hash.max.x = i;
                    for (k in this.map[h]) {
                        ent = this.map[h][k];
                        //make sure that this is a Crafty entity
                        if (typeof ent == 'object' && 'requires' in ent) {
                            coords.max.x = Math.max(coords.max.x, ent.x + ent.w);
                        }
                    }
                }
                if (i <= hash.min.x) {
                    hash.min.x = i;
                    for (k in this.map[h]) {
                        ent = this.map[h][k];
                        if (typeof ent == 'object' && 'requires' in ent) {
                            coords.min.x = Math.min(coords.min.x, ent.x);
                        }
                    }
                }
                if (j >= hash.max.y) {
                    hash.max.y = j;
                    for (k in this.map[h]) {
                        ent = this.map[h][k];
                        if (typeof ent == 'object' && 'requires' in ent) {
                            coords.max.y = Math.max(coords.max.y, ent.y + ent.h);
                        }
                    }
                }
                if (j <= hash.min.y) {
                    hash.min.y = j;
                    for (k in this.map[h]) {
                        ent = this.map[h][k];
                        if (typeof ent == 'object' && 'requires' in ent) {
                            coords.min.y = Math.min(coords.min.y, ent.y);
                        }
                    }
                }
            }

            return coords;
        }
    };

/**@
* #Crafty.HashMap
* @category 2D
* Broad-phase collision detection engine. See background information at
*
* ~~~
* - [N Tutorial B - Broad-Phase Collision](http://www.metanetsoftware.com/technique/tutorialB.html)
* - [Broad-Phase Collision Detection with CUDA](http.developer.nvidia.com/GPUGems3/gpugems3_ch32.html)
* ~~~
* @see Crafty.map
*/

    /**@
    * #Crafty.HashMap.key
    * @comp Crafty.HashMap
    * @sign public Object Crafty.HashMap.key(Object obj)
    * @param obj - an Object that has .mbr() or _x, _y, _w and _h.
    * Get the rectangular region (in terms of the grid, with grid size `cellsize`), where the object may fall in. This region is determined by the object's bounding box.
    * The `cellsize` is 64 by default.
    *
    * @see Crafty.HashMap.constructor
    */
    HashMap.key = function (obj) {
        if (obj.hasOwnProperty('mbr')) {
            obj = obj.mbr();
        }
        var x1 = Math.floor(obj._x / cellsize),
        y1 = Math.floor(obj._y / cellsize),
        x2 = Math.floor((obj._w + obj._x) / cellsize),
        y2 = Math.floor((obj._h + obj._y) / cellsize);
        return { x1: x1, y1: y1, x2: x2, y2: y2 };
    };

    HashMap.hash = function (keys) {
        return keys.x1 + SPACE + keys.y1 + SPACE + keys.x2 + SPACE + keys.y2;
    };

    function Entry(keys, obj, map) {
        this.keys = keys;
        this.map = map;
        this.obj = obj;
    }

    Entry.prototype = {
        update: function (rect) {
            //check if buckets change
            if (HashMap.hash(HashMap.key(rect)) != HashMap.hash(this.keys)) {
                this.map.remove(this.keys, this.obj);
                var e = this.map.insert(this.obj);
                this.keys = e.keys;
            }
        }
    };

    parent.HashMap = HashMap;
})(Crafty);


