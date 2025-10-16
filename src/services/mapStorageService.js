import { db, storage } from '../firebase';
import { collection, addDoc, query, where, getDocs, orderBy, limit, Timestamp, updateDoc, doc } from 'firebase/firestore';
import { ref, uploadString, getDownloadURL } from 'firebase/storage';

class MapStorageService {
  constructor() {
    this.mapsCollection = 'land_layout_maps';
    this.mapStorageFolder = 'land-layout-maps';
  }

  /**
   * Store map data in Firebase Firestore
   * @param {Object} mapData - The map data to store
   * @returns {Promise<string>} - The document ID of the stored map
   */
  async storeMapData(mapData) {
    try {
      const mapDoc = {
        ...mapData,
        created_at: Timestamp.now(),
        updated_at: Timestamp.now()
      };

      const docRef = await addDoc(collection(db, this.mapsCollection), mapDoc);
      console.log('Map data stored with ID: ', docRef.id);
      return docRef.id;
    } catch (error) {
      console.error('Error storing map data: ', error);
      throw error;
    }
  }

  /**
   * Store map HTML file in Firebase Storage
   * @param {string} mapHtml - The HTML content of the map
   * @param {string} mapId - The ID of the map
   * @returns {Promise<string>} - The download URL of the stored map file
   */
  async storeMapFile(mapHtml, mapId) {
    try {
      // Create a reference to the map file in Firebase Storage
      const mapFileRef = ref(storage, `${this.mapStorageFolder}/${mapId}.html`);
      
      // Upload the HTML content as a string
      await uploadString(mapFileRef, mapHtml, 'raw');
      
      // Get the download URL
      const downloadURL = await getDownloadURL(mapFileRef);
      console.log('Map file stored at: ', downloadURL);
      return downloadURL;
    } catch (error) {
      console.error('Error storing map file: ', error);
      throw error;
    }
  }

  /**
   * Store both map data and map file
   * @param {Object} mapData - The map data to store
   * @param {string} mapFilePath - The path to the map HTML file
   * @returns {Promise<Object>} - Object containing document ID and download URL
   */
  async storeMap(mapData, mapFilePath) {
    try {
      // Read the HTML file content
      const response = await fetch(mapFilePath);
      const mapHtml = await response.text();
      
      // Store map data in Firestore
      const mapId = await this.storeMapData(mapData);
      
      // Store map file in Firebase Storage
      const downloadURL = await this.storeMapFile(mapHtml, mapId);
      
      // Update the map data with the file URL
      const mapDocRef = doc(db, this.mapsCollection, mapId);
      await updateDoc(mapDocRef, {
        map_file_url: downloadURL,
        updated_at: Timestamp.now()
      });
      
      return {
        id: mapId,
        url: downloadURL
      };
    } catch (error) {
      console.error('Error storing map: ', error);
      throw error;
    }
  }

  /**
   * Retrieve map data by ID
   * @param {string} mapId - The ID of the map to retrieve
   * @returns {Promise<Object|null>} - The map data or null if not found
   */
  async getMapData(mapId) {
    try {
      const mapQuery = query(
        collection(db, this.mapsCollection),
        where('__name__', '==', mapId)
      );
      
      const querySnapshot = await getDocs(mapQuery);
      
      if (querySnapshot.empty) {
        console.log('No map found with ID: ', mapId);
        return null;
      }
      
      const doc = querySnapshot.docs[0];
      return {
        id: doc.id,
        ...doc.data()
      };
    } catch (error) {
      console.error('Error retrieving map data: ', error);
      throw error;
    }
  }

  /**
   * Retrieve recent maps
   * @param {number} limitCount - Number of maps to retrieve
   * @returns {Promise<Array>} - Array of map records
   */
  async getRecentMaps(limitCount = 10) {
    try {
      const mapsQuery = query(
        collection(db, this.mapsCollection),
        orderBy('created_at', 'desc'),
        limit(limitCount)
      );
      
      const querySnapshot = await getDocs(mapsQuery);
      const mapsData = [];
      
      querySnapshot.forEach((doc) => {
        mapsData.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return mapsData;
    } catch (error) {
      console.error('Error retrieving maps: ', error);
      throw error;
    }
  }

  /**
   * Update map data
   * @param {string} mapId - The ID of the map to update
   * @param {Object} updateData - The data to update
   * @returns {Promise<void>}
   */
  async updateMap(mapId, updateData) {
    try {
      const mapDocRef = doc(db, this.mapsCollection, mapId);
      await updateDoc(mapDocRef, {
        ...updateData,
        updated_at: Timestamp.now()
      });
      console.log('Map updated with ID: ', mapId);
    } catch (error) {
      console.error('Error updating map: ', error);
      throw error;
    }
  }
}

export default new MapStorageService();